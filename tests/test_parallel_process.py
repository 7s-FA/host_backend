"""Dependency, resource, failure and replay tests; no network or robot commands."""
import json
from pathlib import Path
import random
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_process import FakeTransport
from parallel_process import ParallelProcessController, dependencies, resources
from control import ProcessController

OK = dict(status=4, success=True, message='IDLE')
ERROR = dict(status=6, success=False, message='ERROR')


class CorrelatedTransport(FakeTransport):
    def stop(self, device):
        super().stop(device)
        return f'stop-{len(self.stops)}'


class ParallelTest(unittest.TestCase):
    def setUp(self):
        self.now = 0
        self.transport = CorrelatedTransport()
        self.core = ParallelProcessController(self.transport, clock=lambda: self.now,
                                             goal_timeout=2, motion_timeout=5, arm_timeout=5)
        self.core.tick(True)

    def command(self, action, **extra):
        self.core.command(dict(id=f'cmd-{len(self.core.processed)}', action=action,
                               order_id=(self.core.order or {}).get('id'), **extra))

    def start(self, quantity=2, product='A', automatic=True):
        self.command('start', product_type=product, quantity=quantity, auto_advance=automatic)
        self.core.tick(True)

    def indices(self):
        return {task['index'] for task in self.core.inflight.values()}

    def task(self, index):
        return next(t for t in self.core.inflight.values() if t['index'] == index)

    def result(self, index, data=None):
        prep = len(self.core.plan)-1
        if index != prep and prep in self.indices():
            self.result(prep)
        task = self.task(index).copy()
        self.core.event(task['id'], 'accepted', {})
        self.core.event(task['id'], 'done', OK if data is None else data)
        return task

    def phase(self, index):
        task = self.task(index)
        self.core.event(task['id'], 'accepted', {})
        self.core.event(task['id'], 'feedback', {'message':'BUILD_DONE'})

    def tick(self): self.core.tick(True)

    def stop_results(self, data=None):
        for device, (identity, _) in list(self.core.parallel_stops.items()):
            self.core.event(identity, 'stop', dict(OK if data is None else data, device=device))

    def retry(self):
        self.command('retry', stage=self.core.order['stage'],
                     recovery_revision=self.core.order.get('recovery_revision', 0), operator_confirmed=True)
        self.tick()

    def test_first_load_and_m2_rest_overlap_but_m1_waits_for_both(self):
        for first in (1, 2):
            self.setUp(); self.start(); self.result(0); self.tick()
            self.assertEqual(self.indices(), {1, 2})
            self.result(first); self.tick()
            self.assertEqual(self.indices(), {3-first})
            self.result(3-first); self.tick()
            self.assertEqual(self.indices(), {3})

    def test_full_pipeline_overlaps_and_docking_waits_for_clear_cell(self):
        self.start()
        for index in (0, 1, 2, 3): self.result(index); self.tick()
        self.assertEqual(self.indices(), {4, 5}) # arm2 chain + M2 material
        self.assertEqual(self.task(4)['command'], 'BUILD_LOAD_A')
        self.result(5); self.tick(); self.assertEqual(self.indices(), {4, 6})
        self.phase(4); self.tick()
        self.assertEqual(self.indices(), {4, 6, 8}) # chain load + load2 + M1 departure
        self.assertEqual(self.core.order['completed'], 0)
        self.result(8); self.result(6); self.tick()
        self.assertEqual(self.indices(), {4}) # M2 waits for final chain result
        self.result(4); self.tick(); self.assertEqual(self.indices(), {9})
        self.result(9); self.tick(); self.assertEqual(self.indices(), {10, 11})
        self.phase(11); self.tick(); self.assertEqual(self.indices(), {10, 11})
        self.result(10); self.tick(); self.assertEqual(self.indices(), {11, 13})
        self.result(13); self.tick(); self.assertEqual(self.core.order['status'], 'running')
        self.result(11); self.tick(); self.assertEqual(self.core.order['status'], 'done')
        self.assertFalse(any(t['command'].startswith('LOAD_') for t in self.transport.sent))

    def test_single_product_departure_overlaps_final_pallet_loading(self):
        self.start(quantity=1)
        for index in range(3): self.result(index); self.tick()
        self.phase(3); self.tick(); self.assertEqual(self.indices(), {3, 5})
        self.result(5); self.tick()
        self.assertEqual(self.core.order['completed'], 0)
        self.result(3); self.assertEqual(self.core.order['status'], 'done')

    def test_chain_failure_after_build_retries_load_only(self):
        self.start(quantity=1)
        for index in range(3): self.result(index); self.tick()
        self.phase(3); self.tick(); self.result(5)
        self.result(3, ERROR); self.assertTrue(self.core.can_recover())
        self.assertEqual(self.core.failed_steps, {4})
        self.retry(); self.assertEqual(self.indices(), {4})
        self.assertEqual(self.task(4)['command'], 'LOAD_A')
        self.result(4); self.assertEqual(self.core.order['status'], 'done')
        self.assertEqual(self.core.order['completed'], 1)
        self.assertEqual(sum(t['command']=='BUILD_LOAD_A' for t in self.transport.sent), 1)

    def test_only_correlated_accepted_build_milestone_permits_departure(self):
        self.start(quantity=1)
        for index in range(3): self.result(index); self.tick()
        task=self.task(3)
        self.core.event('old','feedback',{'message':'BUILD_DONE'});self.tick()
        self.core.event(task['id'],'feedback',{'message':'BUILD_DONE'});self.tick()
        self.assertEqual(self.indices(),{3})
        self.core.event(task['id'],'accepted',{})
        self.core.event(task['id'],'feedback',{'message':'IDLE'});self.tick()
        self.assertEqual(self.indices(),{3})
        self.phase(3);self.tick();self.assertEqual(self.indices(),{3,5})
        self.assertEqual(self.core.order['completed'],0)

    def test_random_completion_order_preserves_all_dependencies_and_counts(self):
        for quantity in (1, 2):
            for product in ('A', 'B'):
                for seed in range(30):
                    self.setUp(); self.start(quantity, product)
                    rand = random.Random(seed)
                    submitted = 0
                    while self.core.order['status'] != 'done':
                        for task in self.transport.sent[submitted:]:
                            self.assertLessEqual(dependencies(quantity)[task['index']], self.core.finished)
                        submitted = len(self.transport.sent)
                        claims = [resources(self.core.plan[t['index']]) for t in self.core.inflight.values()]
                        self.assertEqual(sum(map(len, claims)), len(set().union(*claims)))
                        chosen = rand.choice(sorted(self.indices()))
                        if self.task(chosen)['command'].startswith('BUILD_LOAD_') and rand.choice((True,False)):
                            self.phase(chosen); self.tick()
                        task = self.result(chosen)
                        self.core.event(task['id'], 'done', OK) # duplicate
                        self.tick()
                    self.assertEqual((self.core.order['completed'], self.core.order['transport_remaining'],
                                      self.core.order['product_remaining']), (quantity, 0, 0))
                    self.assertEqual(len(self.transport.sent), len(self.core.plan)-quantity)

    def test_pause_drains_every_task_without_launching_dependents(self):
        self.start(); self.result(0); self.tick()
        self.command('pause'); self.result(1); self.tick()
        self.assertEqual(self.indices(), {2}); self.assertEqual(self.core.order['status'], 'running')
        self.result(2); self.tick(); self.assertEqual(self.core.order['status'], 'paused')
        self.command('resume'); self.tick(); self.assertEqual(self.indices(), {3})

    def test_manual_progress_waits_for_entire_wave(self):
        self.start(automatic=False); self.result(0); self.tick()
        self.assertEqual(self.core.order['status'], 'waiting')
        self.command('next', stage=self.core.order['stage']); self.tick(); self.assertEqual(self.indices(), {1, 2})
        self.result(1); self.tick(); self.assertFalse(self.core.can_advance())
        self.result(2); self.tick(); self.assertTrue(self.core.can_advance())
        self.assertEqual(self.indices(), set())

    def test_web_disconnect_does_not_launch_or_resume(self):
        self.start(); self.result(0); self.tick()
        self.core.tick(False); self.result(1); self.result(2); self.tick()
        self.assertEqual(self.core.order['status'], 'paused')
        self.assertEqual(len(self.transport.sent), 4)

    def test_failure_stops_siblings_and_successful_sibling_is_not_replayed(self):
        self.start(); self.result(0); self.tick()
        self.result(1, ERROR)
        self.assertEqual(self.transport.stops, ['arm1'])
        self.assertFalse(self.core.can_recover())
        sibling = self.result(2)
        self.stop_results(); self.assertTrue(self.core.can_recover())
        self.retry(); self.assertEqual(self.indices(), {1})
        self.core.event(sibling['id'], 'done', OK)
        self.result(1); self.tick(); self.assertEqual(self.indices(), {3})
        self.assertEqual(sum(t['index']==2 for t in self.transport.sent), 1)

    def test_uncertain_result_never_releases_aisle_or_enables_retry(self):
        self.start(); self.result(14); task = self.task(0)
        self.core.event(task['id'], 'accepted', {})
        self.core.event(task['id'], 'done', dict(ERROR, uncertain=True)); self.stop_results()
        self.assertFalse(self.core.can_recover()); self.assertEqual(self.indices(), {0})
        self.core.event(task['id'], 'done', ERROR)
        self.assertTrue(self.core.can_recover())

    def test_reset_requires_all_correlated_stops_and_archives_all_tasks(self):
        with tempfile.TemporaryDirectory() as folder:
            self.core.state_file = Path(folder)/'state.json'
            self.start(); self.result(0); self.tick()
            for task in self.core.inflight.values(): self.core.event(task['id'], 'accepted', {})
            self.core.fail('test'); self.stop_results(ERROR)
            self.assertTrue(self.core.can_reset())
            self.command('reset', operator_confirmed=True)
            self.assertTrue(self.core.reset_pending)
            self.core.event('wrong', 'stop', dict(OK, device='M2'))
            self.assertIsNotNone(self.core.order) # Unrelated stop responses cannot release either task.
            self.stop_results()
            self.assertIsNone(self.core.order)
            archive = json.loads(next((Path(folder)/'order-history').glob('*.json')).read_text())
            self.assertEqual(len(archive['parallel_state']['inflight']), 2)
            saved = json.loads(self.core.state_file.read_text())
            self.assertFalse(saved['parallel_state']['inflight'])

    def test_timeout_and_late_acceptance_stop_every_device_without_new_work(self):
        self.start(); self.result(0); self.tick(); self.now = 3; self.tick()
        self.assertEqual(set(self.transport.stops), {'M2', 'arm1'})
        count = len(self.transport.sent)
        self.stop_results(); self.assertFalse(self.core.can_recover())
        task = self.task(2); self.core.event(task['id'], 'accepted', {})
        self.assertEqual(self.transport.stops[-1], 'arm1')
        self.tick(); self.assertEqual(len(self.transport.sent), count)

    def test_transport_count_retry_is_idempotent(self):
        self.start()
        for i in (0, 1, 2): self.result(i); self.tick()
        self.result(3, ERROR); self.assertEqual(self.core.order['transport_remaining'], 1)
        self.retry(); self.result(3); self.assertEqual(self.core.order['transport_remaining'], 1)

    def test_restart_stops_all_unfinished_tasks_never_replays_completed_work(self):
        with tempfile.TemporaryDirectory() as folder:
            self.core.state_file = Path(folder)/'state.json'
            self.start(); self.result(0); self.tick()
            old_transport = self.transport
            self.transport = CorrelatedTransport()
            self.core = ParallelProcessController(self.transport, state_file=self.core.state_file)
            self.tick(); self.assertEqual(set(self.transport.stops), {'M2', 'arm1'})
            self.assertEqual(self.transport.sent, [])
            self.assertEqual(self.core.finished, {0,14})
            self.assertFalse(self.core.can_recover())
            self.stop_results(); self.assertTrue(self.core.can_recover())
            self.retry(); self.assertEqual(self.indices(), {1, 2})
            self.assertEqual(len(old_transport.sent), 4)

    def test_legacy_order_stays_serial_on_restore(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'state.json'
            legacy = ProcessController(self.transport, state_file=path)
            legacy.tick(True); legacy.command(dict(id='old', action='start', product_type='A', quantity=2))
            legacy.tick(True)
            resumed = ParallelProcessController(CorrelatedTransport(), state_file=path)
            self.assertFalse(resumed.parallel_order())
            self.assertEqual(resumed.order['stage'], 0)

    def test_done_order_manual_restart_keeps_unconfirmed_stop_locked(self):
        for response in ('error', 'timeout'):
            with self.subTest(response=response), tempfile.TemporaryDirectory() as folder:
                self.setUp(); self.start(quantity=1)
                while self.core.order['status'] != 'done':
                    self.result(min(self.indices())); self.tick()
                path = Path(folder)/'state.json'; self.core.state_file = path
                self.command('manual_move', stage=self.core.order['stage'], recovery_revision=0,
                             operator_confirmed=True, device='M1', destination='GO_TO_PARK')
                self.transport = CorrelatedTransport()
                self.core = ParallelProcessController(self.transport, state_file=path, clock=lambda:self.now)
                self.tick()
                self.assertIsNotNone(self.core.stop_request)
                if response == 'error':
                    self.core.event(self.core.stop_request[0], 'stop', dict(ERROR,device='M1'))
                else:
                    self.now += 16
                self.tick(); self.tick()
                self.assertFalse(self.core.can_manual_move())
                self.assertFalse(self.core.snapshot()['can_start'])
                self.assertTrue(self.core.recovery_uncertain)
                self.assertIsNone(self.core.stop_request)

    def test_failed_order_manual_restart_reset_waits_for_manual_stop(self):
        with tempfile.TemporaryDirectory() as folder:
            self.start(); self.result(0, ERROR)
            path = Path(folder)/'state.json'; self.core.state_file = path
            self.command('manual_move', stage=self.core.order['stage'], recovery_revision=0, operator_confirmed=True,
                         device='M2', destination='GO_TO_PARK')
            self.transport = CorrelatedTransport()
            self.core = ParallelProcessController(self.transport, state_file=path)
            self.tick()
            self.core.event(self.core.stop_request[0], 'stop', dict(ERROR,device='M2'))
            self.tick()
            self.assertFalse(self.core.can_recover())
            self.command('reset', operator_confirmed=True)
            self.assertIsNotNone(self.core.order)
            self.assertTrue(self.core.reset_pending)
            self.assertIsNotNone(self.core.stop_request)
            self.core.event(self.core.stop_request[0], 'stop', dict(OK,device='M2'))
            self.assertIsNone(self.core.order)

    def test_restart_after_chain_handoff_never_rebuilds(self):
        with tempfile.TemporaryDirectory() as folder:
            self.core.state_file = Path(folder)/'state.json'
            self.start(quantity=1)
            for i in range(3): self.result(i); self.tick()
            self.phase(3); self.tick()
            self.transport = CorrelatedTransport()
            self.core = ParallelProcessController(self.transport,state_file=self.core.state_file)
            self.tick(); self.assertEqual(set(self.transport.stops), {'arm2','M1'})
            self.stop_results(); self.retry()
            self.assertEqual(self.indices(), {4,5})
            self.assertEqual({t['command'] for t in self.transport.sent}, {'LOAD_A','GO_TO_PARK'})

    def test_linear_preparation_starts_with_first_drive_and_gates_build(self):
        self.start()
        self.assertEqual(self.indices(), {0,14})
        self.assertEqual(self.task(14)['command'], 'BUILD_SLIDE')
        # Hold the linear result while completing the independent warehouse route.
        for i in (0,1,2,3):
            t=self.task(i)
            self.core.event(t['id'],'accepted',{})
            self.core.event(t['id'],'done',OK);self.tick()
        self.assertIn(14,self.indices())
        self.assertNotIn(4,self.indices())
        self.result(14);self.tick()
        self.assertIn(4,self.indices())
        self.assertEqual(sum(t['command']=='BUILD_SLIDE' for t in self.transport.sent),1)

    def test_linear_preparation_failure_stops_initial_drive(self):
        self.start();self.result(14,ERROR)
        self.assertEqual(self.core.order['status'],'failed')
        self.assertEqual(self.transport.stops,['M1'])
        self.assertFalse(any(t['command'].startswith('BUILD_LOAD_') for t in self.transport.sent))

    def test_report_shows_every_concurrent_device(self):
        self.start(); self.result(0); self.tick()
        report = self.core.snapshot()
        self.assertEqual(report['devices']['M2']['state'], 'running')
        self.assertEqual(report['devices']['warehouse']['state'], 'running')
        self.assertIn('동시 작업', report['order']['stage_label'])
        self.assertFalse(report['can_manual_move']); self.assertFalse(report['can_start'])

if __name__ == '__main__': unittest.main()

# The runtime replacement must retain the idle/done manual-control contract.
from test_idle_manual import IdleManualTest as _IdleManualTest
class ParallelIdleManualTest(_IdleManualTest):
    def setUp(self):
        super().setUp()
        self.core = ParallelProcessController(self.transport, clock=lambda:self.now,
                                             goal_timeout=2,motion_timeout=5,arm_timeout=5)
        self.core.tick(True)
