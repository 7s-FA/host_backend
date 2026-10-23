import unittest
import random
import tempfile
from pathlib import Path
from collections import Counter
from test_parallel_process import CorrelatedTransport, OK, ERROR, resources
from continuous_process import ContinuousProcessController

class ContinuousTest(unittest.TestCase):
    def setUp(self):
        self.transport=CorrelatedTransport()
        self.core=ContinuousProcessController(self.transport)
        self.core.tick(True)
        self.sequence=0
    def command(self,action,**extra):
        self.sequence+=1
        cmd=dict(id=f'cmd-{self.sequence}',action=action,**extra)
        self.core.command(cmd)
        return cmd
    def start(self,a=1,b=0,automatic=True):
        self.command('start',quantities={'A':a,'B':b},auto_advance=automatic)
    def tick(self):
        self.core.tick(True)
        occupied=set()
        for t in self.core.inflight.values():
            claims=resources(self.core.plan[t['index']])
            self.assertFalse(occupied & claims, self.core.inflight)
            occupied |= claims
    def complete(self,t):
        self.core.event(t['id'],'accepted',{})
        self.core.event(t['id'],'done',OK)
    def finish(self):
        for _ in range(100):
            self.tick()
            for t in list(self.core.inflight.values()): self.complete(t)
            if self.core.order['status']=='done':return
        self.fail((self.core.order,self.core.inflight,self.core.finished))
    def check_counts(self,products):
        self.assertEqual(self.core.order['products'],products)
        self.assertEqual(self.core.order['completed'],len(products))
        counts=Counter((t['device'],t['command']) for t in self.transport.sent)
        self.assertEqual(counts['arm2','BUILD_SLIDE'],1)
        for p in ('A','B'):
            self.assertEqual(counts['arm1','SELECT_'+p],products.count(p))
            self.assertEqual(counts['arm2','BUILD_LOAD_'+p],products.count(p))
        for robot,n in [('M1',(len(products)+1)//2),('M2',len(products)//2)]:
            self.assertEqual(counts[robot,'GO_TO_MAT'],n)
            self.assertEqual(counts[robot,'GO_TO_ASM'],n)
        self.assertFalse(any(t['command'].startswith('LOAD_') for t in self.transport.sent))
        self.assertFalse(self.core.pending_batches)
    def test_all_sizes_and_mix(self):
        for a,b in [(1,0),(0,1),(2,0),(0,2),(1,1),(2,1),(1,2),(2,2)]:
            with self.subTest(a=a,b=b):
                self.setUp();self.start(a,b);self.finish();self.check_counts(['A']*a+['B']*b)
    def test_append_at_every_phase_and_no_duplicate_callbacks(self):
        for steps in range(6):
            with self.subTest(steps=steps):
                self.setUp();self.start()
                for _ in range(steps):
                    self.tick()
                    for t in list(self.core.inflight.values()):self.complete(t)
                self.tick()
                if self.core.order['status']=='done':continue
                ids=set(self.core.inflight)
                cmd=self.command('enqueue',quantities={'A':1,'B':2})
                self.core.command(cmd)
                self.assertEqual(set(self.core.inflight),ids)
                self.finish();self.check_counts(['A','A','B','B'])
    def test_append_after_return_issued_and_completed(self):
        for parked in (False,True):
            self.setUp();self.start()
            for _ in range(3):
                self.tick()
                for t in list(self.core.inflight.values()):self.complete(t)
            self.tick()
            build=next(t for t in self.core.inflight.values() if t['command']=='BUILD_LOAD_A')
            self.core.event(build['id'],'accepted',{})
            self.core.event(build['id'],'feedback',{'message':'BUILD_DONE'})
            self.tick()
            park=next(t for t in self.core.inflight.values() if t['command']=='GO_TO_PARK')
            if parked:self.complete(park)
            self.command('enqueue',quantities={'A':0,'B':1})
            self.tick()
            if not parked:
                self.assertFalse(any(t['device']=='M2' for t in self.transport.sent))
                self.complete(park)
            self.finish();self.check_counts(['A','B'])
            self.assertEqual(sum(t['device']=='M1' and t['command']=='GO_TO_PARK' for t in self.transport.sent),1)
    def test_random_append_with_partial_build_results(self):
        for seed in range(40):
            self.setUp();rng=random.Random(seed);self.start()
            additions=['B','A','B']
            for _ in range(160):
                if additions and self.core.appendable() and rng.random()<.22:
                    p=additions.pop(0);self.command('enqueue',quantities={k:int(k==p) for k in ('A','B')})
                self.tick()
                tasks=list(self.core.inflight.values())
                if tasks:
                    t=rng.choice(tasks)
                    self.core.event(t['id'],'accepted',{})
                    if t['command'].startswith('BUILD_LOAD_') and not t.get('build_done'):
                        self.core.event(t['id'],'feedback',{'message':'BUILD_DONE'})
                    else:self.complete(t)
                if self.core.order['status']=='done':break
            self.assertEqual(self.core.order['status'],'done',seed)
            self.check_counts(['A']+['B','A','B'][:3-len(additions)])
    def test_per_product_limit_includes_prior_submissions(self):
        self.start(1,1)
        self.command('enqueue',quantities={'A':1,'B':0})
        bad=self.command('enqueue',quantities={'A':1,'B':1})
        self.assertIn(bad['id'],self.core.rejected)
        self.assertEqual(self.core.order['products'],['A','B','A'])
        self.command('enqueue',quantities={'A':0,'B':1})
        self.assertFalse(self.core.can_enqueue())
        self.finish();self.check_counts(['A','B','A','B'])

    def test_append_reuses_robot_after_terminal_parking_was_issued(self):
        for initial in ((1,1),(2,1)):
            self.setUp();self.start(*initial)
            for _ in range(70):
                self.tick()
                parking=[t for t in self.core.inflight.values() if t['command']=='GO_TO_PARK']
                if parking:break
                for t in list(self.core.inflight.values()):
                    self.core.event(t['id'],'accepted',{})
                    if t['command'].startswith('BUILD_LOAD_') and not t.get('build_done'):
                        self.core.event(t['id'],'feedback',{'message':'BUILD_DONE'})
                    else:self.complete(t)
            self.assertTrue(parking)
            self.command('enqueue',quantities={'A':2-initial[0],'B':2-initial[1]})
            self.finish()
            self.check_counts(['A']*initial[0]+['B']*initial[1]+['A']*(2-initial[0])+['B']*(2-initial[1]))
    def test_pause_manual_and_failed_never_auto_resume(self):
        for state in ('paused','waiting','failed'):
            self.setUp();self.start(automatic=False)
            self.core.order.update(status=state,pause_requested=state=='paused')
            self.command('enqueue',quantities={'A':0,'B':1})
            self.tick();self.assertEqual(self.transport.sent,[])
            self.assertFalse(self.core.order['auto_advance'])
            self.assertEqual(self.core.order['quantity'],1 if state=='failed' else 2)
    def test_restore_four_product_plan_no_motion_replay(self):
        with tempfile.TemporaryDirectory() as directory:
            self.core.state_file=Path(directory)/'state.json'
            self.start(2,2);self.tick()
            restored=ContinuousProcessController(CorrelatedTransport(),state_file=self.core.state_file)
            self.assertEqual(restored.order['quantity'],4)
            self.assertEqual(len(restored.plan),len(self.core.plan))
            self.assertEqual(restored.order['status'],'failed')
            restored.tick(True);self.assertFalse(restored.transport.sent)
    def test_failure_after_build_done_keeps_loading_retry(self):
        self.start()
        for _ in range(3):
            self.tick()
            for t in list(self.core.inflight.values()):self.complete(t)
        self.tick();t=next(t for t in self.core.inflight.values() if t['command']=='BUILD_LOAD_A')
        self.core.event(t['id'],'accepted',{})
        self.core.event(t['id'],'feedback',{'message':'BUILD_DONE'})
        self.command('enqueue',quantities={'A':1,'B':2})
        self.core.event(t['id'],'done',ERROR)
        self.assertEqual(self.core.failed_steps,{self.core.order_load_index(t['index'])})
        self.assertEqual(self.core.order['status'],'failed')
