"""One appendable order, A <= 2 and B <= 2; alternate AMRs without pallet batches."""
from dataclasses import asdict
from control import Step
from queued_process import QueuedProcessController, selected_products

MODE = 'continuous-v1'


def graph(products, previous=None, committed=()):
    previous = previous or {}
    old_keys = previous.get('process_keys', [])
    old = {key: (previous['process_plan'][i],
                 {old_keys[j] for j in previous['process_dependencies'][i]})
           for i, key in enumerate(old_keys)}
    committed = set(committed)
    nodes, deps = {}, {}

    def add(key, device, command, number, label, requires=()):
        nodes[key] = asdict(Step(device, command, number, label))
        deps[key] = set(requires)
        if key in committed:
            nodes[key], deps[key] = old[key][0].copy(), old[key][1].copy()

    def key(i, phase): return f'{i}:{phase}'
    def robot(i): return 'M1' if i % 2 else 'M2'
    def parked_leave(i):
        k = key(i, 'leave')
        return k in committed and old[k][0]['command'] == 'GO_TO_PARK'

    count = len(products)
    add('prepare', 'arm2', 'BUILD_SLIDE', 0, '리니어 조립 위치 사전 준비')
    if count > 1:
        stage_deps = {key(1, 'mat')}
        if parked_leave(1): stage_deps.add(key(1, 'leave'))
        add('stage:M2', 'M2', 'GO_TO_REST', 2, 'M2 대기장소 주차', stage_deps)
    for i, product in enumerate(products, 1):
        amr = robot(i)
        mat_deps = set() if i == 1 else {key(i-1, 'asm')}
        if i == 2: mat_deps.add('stage:M2')
        if i > 2: mat_deps.add(key(i-2, 'leave'))
        if i > 1 and parked_leave(i-1): mat_deps.add(key(i-1, 'leave'))
        # A parking request issued before an append is never canceled or replayed.
        if i > 2 and f'park:{amr}' in committed: mat_deps.add(f'park:{amr}')
        add(key(i,'mat'),amr,'GO_TO_MAT',i,f'{i}번 {amr} 자재창고 도킹',mat_deps)
        add(key(i,'select'),'arm1','SELECT_'+product,i,f'{i}번 자재 적재',{key(i,'mat')})
        asm_deps = {key(i,'select')}
        if i == 1 and count > 1: asm_deps.add('stage:M2')
        if i > 1: asm_deps |= {key(i-1,'load'),key(i-1,'leave')}
        add(key(i,'asm'),amr,'GO_TO_ASM',i,f'{i}번 {amr} 제작공정 도킹',asm_deps)
        add(key(i,'build'),'arm2','BUILD_LOAD_'+product,i,f'{i}번 조립·적재 연속',{key(i,'asm'),'prepare'})
        add(key(i,'load'),'arm3','LOAD_'+product,i,f'{i}번 완제품 팔레트 적재',{key(i,'build')})
        leave_deps = {key(i,'build')}
        if i < count: leave_deps.add(key(i+1,'mat'))
        add(key(i,'leave'),amr,'GO_TO_PARK' if i == count else 'GO_TO_REST',i,
            f'{i}번 {amr} '+('초기위치 복귀' if i==count else '대기장소 주차'),leave_deps)
    # Retain already-issued terminal parking even when that AMR is reused.
    for k in committed:
        if k not in nodes:
            nodes[k],deps[k]=old[k][0].copy(),old[k][1].copy()
    if count > 1:
        other = robot(count-1)
        if nodes[key(count-1,'leave')]['command'] == 'GO_TO_PARK':
            parked = key(count-1,'leave')
        else:
            parked = f'park:{other}'
            # A previous early return cannot stand in for parking after reuse.
            if parked in committed and count > 3:
                parked += f':after{count-1}'
            add(parked,other,'GO_TO_PARK',count-1,f'{other} 초기위치 복귀',
                {key(count,'asm'),key(count-1,'leave')})
        if key(count,'leave') not in committed:
            deps[key(count,'leave')].add(parked)
    keys = [k for k in old_keys if k in nodes] + [k for k in nodes if k not in old_keys]
    indices = {k:i for i,k in enumerate(keys)}
    return dict(process_keys=keys,process_plan=[nodes[k] for k in keys],
                process_dependencies=[sorted(indices[d] for d in deps[k]) for k in keys],
                process_load_steps={str(indices[key(i,'build')]):indices[key(i,'load')] for i in range(1,count+1)})


class ContinuousProcessController(QueuedProcessController):
    def continuous_order(self):
        return bool(self.order and self.order.get('plan_mode') == MODE)

    def appendable(self):
        return bool(self.continuous_order() and self.order['status'] in ('running','waiting','paused')
                    and self.link and not self.manual_inspection and not self.reset_busy()
                    and not self.reset_pending and not self.recovery_uncertain and not self.recovery_stop
                    and not self.stop_request and not self.reset_stop_device and not self.orphans
                    and not self.parallel_stops and not self.pending_stops and not self.unconfirmed
                    and not self.failed_steps and not (self.active or {}).get('manual')
                    and (self.full_reset or {}).get('status') != 'failed')

    def remaining_capacity(self):
        if self.continuous_order() and self.order['status'] != 'done':
            return {p:2-self.order['products'].count(p) for p in ('A','B')}
        return {'A':2,'B':2}

    def can_enqueue(self):
        return self.appendable() and any(self.remaining_capacity().values())

    def can_next_batch(self):
        return False  # Legacy queues require explicit removal, never automatic motion.

    def install_graph(self, products, extending=False):
        old_keys = self.order.get('process_keys', [])
        committed_indices = self.finished | {t['index'] for t in self.inflight.values()}
        committed = {old_keys[i] for i in committed_indices} if extending else set()
        updated = graph(products, self.order if extending else None, committed)
        if extending:
            indices = {k:i for i,k in enumerate(updated['process_keys'])}
            remap = {i:indices[k] for i,k in enumerate(old_keys) if k in indices}
            self.finished = {remap[i] for i in self.finished}
            self.accepted_transports = {remap[i] for i in self.accepted_transports}
            for task in self.inflight.values(): task['index'] = remap[task['index']]
        self.order.update(updated, plan_mode=MODE,products=products,quantity=len(products),
                          stage_count=len(updated['process_keys']),stage=len(self.finished),
                          transport_remaining=len(products)-len(self.accepted_transports),
                          product_remaining=len(products)-self.order['completed'])
        self.plan = [Step(**step) for step in updated['process_plan']]
        if extending:
            self.order['recovery_revision'] = self.order.get('recovery_revision',0)+1
            self.sync_active()

    def command(self, command):
        action, identity = command.get('action'),command.get('id')
        if action not in ('start','enqueue') or (action=='start' and 'quantities' not in command):
            return super().command(command)
        if not isinstance(identity,str) or not identity or identity in self.processed: return
        self.queue_transaction = True
        try:
            products = selected_products(command.get('quantities'))
            automatic = command.get('auto_advance',True)
            if type(automatic) is not bool: raise ValueError('auto_advance 형식 오류')
            if action == 'enqueue':
                if not self.appendable(): raise ValueError('진행 중인 연속 주문에만 추가할 수 있습니다.')
                combined = self.order['products'] + products
                if any(combined.count(p)>2 for p in ('A','B')):
                    raise ValueError('추가 주문을 포함해 A 최대 2개·B 최대 2개입니다.')
                self.install_graph(combined,extending=True)
                self.queue_revision += 1
                self.note('주문 추가 · '+' · '.join(f'{p} {products.count(p)}개' for p in ('A','B') if products.count(p))+' · 기존 공정에 이어서 생산')
            else:
                # Reuse the existing start readiness checks; replace the plan
                # atomically before tick can submit any physical request.
                legacy = dict(id=identity,action='start',product_type=products[0],quantity=min(2,len(products)),
                              products=products[:2],auto_advance=automatic)
                super().command(legacy)
                if identity not in self.rejected:
                    self.install_graph(products)
                    self.note('연속 주문 · A 최대 2개·B 최대 2개 · M1/M2 교대 운반')
        except (ValueError,TypeError) as exc:
            self.rejected.append(identity);self.note('주문 지시 거절 · '+str(exc))
        finally:
            if identity not in self.processed:self.processed.append(identity)
            self.queue_transaction=False;self.save()

    def snapshot(self):
        report=super().snapshot()
        report.update(supports_continuous_orders=True,remaining_capacity=self.remaining_capacity(),
                      can_enqueue=self.can_enqueue(),can_next_batch=False)
        return report
