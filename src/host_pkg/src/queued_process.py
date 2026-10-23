"""Durable FIFO batches. Only explicit pallet-clear confirmation starts a queued batch."""
import json
from pathlib import Path
from movement_reset import MovementResetController

MAX_PENDING = 32


def selected_products(quantities):
    if (not isinstance(quantities, dict) or set(quantities) != {'A', 'B'}
            or any(type(v) is not int or not 0 <= v <= 2 for v in quantities.values())
            or sum(quantities.values()) == 0):
        raise ValueError('A·B 각각 0~2개, 합계 1개 이상 선택하세요.')
    return ['A'] * quantities['A'] + ['B'] * quantities['B']


class QueuedProcessController(MovementResetController):
    def __init__(self, *args, **kwargs):
        path = kwargs.get('state_file')
        saved = json.loads(Path(path).read_text()) if path and Path(path).exists() else {}
        self.pending_batches = saved.get('pending_batches', [])
        self.queue_revision = saved.get('queue_revision', 0)
        self.queue_transaction = False
        super().__init__(*args, **kwargs)

    def extra_state(self):
        return {**super().extra_state(), 'pending_batches': self.pending_batches,
                'queue_revision': self.queue_revision}

    def save(self):
        if not self.queue_transaction:
            super().save()

    def clear_extra_state(self):
        super().clear_extra_state()
        self.pending_batches.clear()
        self.queue_revision += 1

    def can_enqueue(self):
        return bool(self.link and not self.manual_inspection and not self.reset_busy()
                    and sum(len(b['products']) for b in self.pending_batches) <= MAX_PENDING - 4)

    def can_next_batch(self):
        return bool(self.pending_batches and super().snapshot()['can_start'])

    def command(self, command):
        action, identity = command.get('action'), command.get('id')
        special = action in ('enqueue', 'next_batch', 'clear_queue') or (action == 'start' and 'quantities' in command)
        if not special:
            if action == 'start' and self.pending_batches:
                # A legacy client must not bypass a waiting batch.
                command = dict(command, action='unsupported_queue_bypass')
            return super().command(command)
        if not isinstance(identity, str) or not identity or identity in self.processed:
            return
        self.queue_transaction = True
        try:
            if not self.link or self.manual_inspection or self.reset_busy():
                raise ValueError('Host 연결·운영 모드·초기화 종료를 확인하세요.')
            if action in ('next_batch', 'clear_queue'):
                if (type(command.get('queue_revision')) is not int or command['queue_revision'] != self.queue_revision
                        or command.get('order_id') != (self.order or {}).get('id')
                        or command.get('operator_confirmed') is not True):
                    raise ValueError('대기 주문 또는 현재 주문이 변경됐습니다. 다시 확인하세요.')
                if action == 'clear_queue':
                    self.pending_batches.clear()
                    self.queue_revision += 1
                    self.note('대기 주문 삭제 · 진행 중 묶음 유지')
                else:
                    if not self.can_next_batch():
                        raise ValueError('현재 묶음 완료·장치 준비 후 팔레트를 비우고 진행하세요.')
                    batch = self.pending_batches[0]
                    self.start_batch(command, batch)
                    if identity not in self.rejected:
                        self.pending_batches.pop(0)
                        self.queue_revision += 1
            else:
                products = selected_products(command.get('quantities'))
                automatic = command.get('auto_advance', True)
                if type(automatic) is not bool:
                    raise ValueError('auto_advance 형식 오류')
                batches = [dict(products=products[i:i+2], auto_advance=automatic, request_id=identity)
                           for i in range(0, len(products), 2)]
                if sum(len(b['products']) for b in self.pending_batches) + len(products) > MAX_PENDING:
                    raise ValueError('대기 주문은 최대 32개입니다.')
                if action == 'enqueue':
                    self.pending_batches.extend(batches)
                    self.queue_revision += 1
                    self.note(f'대기 주문 추가 · A {products.count("A")}개 · B {products.count("B")}개')
                else:
                    if self.pending_batches:
                        raise ValueError('대기 주문부터 진행하거나 삭제하세요.')
                    self.start_batch(command, batches[0])
                    if identity not in self.rejected:
                        self.pending_batches.extend(batches[1:])
                        self.queue_revision += 1
        except (ValueError, TypeError) as exc:
            self.rejected.append(identity)
            self.note('주문 지시 거절 · '+str(exc))
        finally:
            if identity not in self.processed:
                self.processed.append(identity)
            self.queue_transaction = False
            self.save()

    def start_batch(self, command, batch):
        products = batch['products']
        super().command(dict(id=command['id'], action='start', product_type=products[0],
                             quantity=len(products), products=products, auto_advance=batch['auto_advance']))

    def snapshot(self):
        report = super().snapshot()
        report.update(supports_order_queue=True, pending_batches=[dict(b, products=list(b['products'])) for b in self.pending_batches],
                      queue_revision=self.queue_revision, can_enqueue=self.can_enqueue(),
                      can_next_batch=bool(self.pending_batches and report['can_start']))
        if self.pending_batches:
            report['can_start'] = False
        return report
