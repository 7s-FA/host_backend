import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src/host_pkg/src'))
from control import ProcessController, DEVICES, make_plan


class FakeTransport:
    def __init__(self):
        self.availability = dict.fromkeys(DEVICES, True)
        self.sent, self.stops = [], []
    def ready(self): return self.availability.copy()
    def send(self, task): self.sent.append(task)
    def stop(self, device): self.stops.append(device)


class ProcessTest(unittest.TestCase):
    def setUp(self):
        self.now = 0.0
        self.transport = FakeTransport()
        self.core = ProcessController(self.transport, clock=lambda: self.now, goal_timeout=2,
                                      motion_timeout=5, arm_timeout=5)
        self.core.tick(True)

    def start(self, product='A', quantity=1, automatic=True):
        self.core.command({'id': 'start', 'action': 'start', 'product_type': product,
                           'quantity': quantity, 'auto_advance': automatic})
        self.core.tick(True)

    def result(self, **changes):
        task = self.core.active.copy()
        self.core.event(task['id'], 'accepted', {})
        data = dict(status=4, success=True, message='IDLE')
        data.update(changes)
        self.core.event(task['id'], 'done', data)
        return task

    def command(self, action, **extra):
        self.core.command({'id': f'{action}-{len(self.core.processed)}', 'action': action,
                           'order_id': self.core.order['id'], **extra})

    def test_reset_rejects_running_unconfirmed_offline_and_unaccepted(self):
        self.start()
        self.command('reset', operator_confirmed=True)
        self.assertEqual(self.core.order['status'], 'running')
        self.core.fail('test failure')
        self.command('reset', operator_confirmed=True)
        self.assertIsNotNone(self.core.active, 'Unknown acceptance cannot be reset')
        self.core.event(self.core.active['id'], 'accepted', {})
        self.core.event(None, 'stop', {'device':'M1','status':4,'success':True,'message':'IDLE'})
        self.command('reset', operator_confirmed=False)
        self.assertIsNotNone(self.core.order)
        self.transport.availability['M2'] = False
        self.core.tick(True)
        self.command('reset', operator_confirmed=True)
        self.assertIsNotNone(self.core.order)

    def test_reset_waits_for_correlated_stop_and_archives_without_motion(self):
        with tempfile.TemporaryDirectory() as directory:
            self.core.state_file = Path(directory) / 'order.json'
            self.start()
            old = self.core.active.copy()
            self.core.event(old['id'], 'accepted', {})
            self.core.fail('lost result')
            self.command('reset', operator_confirmed=True)
            self.assertTrue(self.core.reset_pending)
            self.assertEqual(self.transport.stops, ['M1'])
            self.core.event('other', 'stop', {'device':'M2','status':4,'success':True,'message':'IDLE'})
            self.assertIsNotNone(self.core.order)
            self.core.event(None, 'stop', {'device':'M1','status':4,'success':True,'message':'IDLE'})
            self.assertIsNone(self.core.order)
            self.assertEqual(len(self.transport.sent), 1, 'Reset cannot send a movement goal')
            self.assertEqual(len(list((Path(directory)/'order-history').glob('*.json'))), 1)
            self.assertIsNone(json.loads(self.core.state_file.read_text())['order'])
            self.core.event(old['id'], 'done', {'status':4,'success':True,'message':'IDLE'})
            self.core.tick(True)
            self.assertIsNone(self.core.order)
            self.assertTrue(self.core.snapshot()['can_start'])

    def test_reset_stop_timeout_keeps_failed_order_and_allows_retry(self):
        self.start()
        self.core.event(self.core.active['id'], 'accepted', {})
        self.core.fail('lost result')
        self.command('reset', operator_confirmed=True)
        self.now += 16
        self.core.tick(True)
        self.assertFalse(self.core.reset_pending)
        self.assertEqual(self.core.order['status'], 'failed')
        self.assertTrue(self.core.can_reset())
        self.assertEqual(self.core.reset_stop_device, 'M1')
        self.command('reset', operator_confirmed=True)
        self.core.event(None, 'stop', {'device':'M1','status':6,'success':False,'message':'ERROR'})
        self.assertFalse(self.core.reset_pending)
        self.assertIsNotNone(self.core.order)

    def test_reset_after_terminal_failure_does_not_send_stop_or_move(self):
        self.start()
        self.result(status=6, success=False, message='ERROR')
        self.command('reset', operator_confirmed=True)
        self.assertIsNone(self.core.order)
        self.assertEqual(self.transport.stops, [])
        self.assertEqual(len(self.transport.sent), 1)

    def test_all_four_orders_and_no_repeat(self):
        for product in ('A', 'B'):
            for quantity in (1, 2):
                with self.subTest(product=product, quantity=quantity):
                    self.setUp()
                    self.start(product, quantity)
                    while self.core.order['status'] != 'done':
                        task = self.result()
                        completed = self.core.order['completed']
                        self.core.event(task['id'], 'done', dict(status=4, success=True, message='IDLE'))
                        self.assertEqual(completed, self.core.order['completed'])
                        self.core.tick(True)
                    order = self.core.order
                    self.assertEqual((order['completed'], order['product_remaining'], order['transport_remaining']), (quantity, 0, 0))
                    commands = [(t['device'], t['command']) for t in self.transport.sent]
                    self.assertEqual(commands.count(('arm2', 'BUILD_' + product)), quantity)
                    self.assertEqual(commands.count(('arm3', 'LOAD_' + product)), quantity)
                    self.assertEqual(commands[-1], ('M1' if quantity == 1 else 'M2', 'GO_TO_PARK'))
                    if quantity == 1:
                        self.assertFalse(any(d == 'M2' for d, _ in commands))
                    else:
                        self.assertLess(commands.index(('arm3', 'LOAD_' + product)), commands.index(('M2', 'GO_TO_ASM')))
                        self.assertLess(commands.index(('M2', 'GO_TO_ASM')), commands.index(('M1', 'GO_TO_PARK')))
                    count = len(commands)
                    self.core.command({'id': 'start', 'action': 'start', 'product_type': product, 'quantity': quantity})
                    self.core.tick(True)
                    self.assertEqual(len(self.transport.sent), count)

    def test_arm3_result_required_and_home_required(self):
        self.start()
        while self.core.active['device'] != 'arm3':
            self.result(); self.core.tick(True)
        self.assertEqual(self.core.order['completed'], 0)
        self.core.event(self.core.active['id'], 'feedback', {'message': 'IDLE'})
        self.core.tick(True)
        self.assertEqual(self.core.order['completed'], 0)
        self.result(); self.core.tick(True)
        self.assertEqual(self.core.order['completed'], 1)
        self.assertEqual(self.core.order['status'], 'running')
        self.assertEqual(self.core.active['command'], 'GO_TO_PARK')
        self.result()
        self.assertEqual(self.core.order['status'], 'done')

    def test_pause_finishes_current_action_and_resume_does_not_repeat(self):
        self.start()
        self.command('pause')
        self.assertEqual(self.core.order['status'], 'running')
        self.core.tick(True)
        self.assertEqual(len(self.transport.sent), 1)
        self.result(); self.core.tick(True)
        self.assertEqual(self.core.order['status'], 'paused')
        self.assertEqual(len(self.transport.sent), 1)
        self.command('resume'); self.core.tick(True)
        self.assertEqual(self.transport.sent[-1]['command'], 'SELECT_A')
        self.assertEqual(self.transport.stops, [])

    def test_manual_next_is_idempotent_and_bound_to_stage(self):
        self.start(automatic=False)
        self.result(); self.core.tick(True)
        self.assertTrue(self.core.can_advance())
        self.command('next', stage=0); self.core.tick(True)
        self.assertEqual(len(self.transport.sent), 1)
        self.assertEqual(self.core.snapshot()['rejected_command_ids'], ['next-1'])
        self.command('next', stage=1); self.core.tick(True)
        self.command('next', stage=1); self.core.tick(True)
        self.assertEqual(len(self.transport.sent), 2)

    def test_rejected_manual_step_can_be_requested_after_reconnection(self):
        self.start(automatic=False)
        self.result(); self.core.tick(True)
        self.core.link = False
        self.command('next', stage=1)
        self.core.tick(False)
        self.assertEqual(self.core.order['status'], 'paused')
        self.assertEqual(self.core.snapshot()['rejected_command_ids'], ['next-1'])
        self.core.tick(True)
        self.command('resume')
        self.command('next', stage=1)
        self.core.tick(True)
        self.assertEqual(len(self.transport.sent), 2)
        self.assertEqual(self.transport.sent[-1]['command'], 'SELECT_A')

    def test_http_disconnect_does_not_auto_resume(self):
        self.start()
        self.core.tick(False)
        self.result(); self.core.tick(True)
        self.assertEqual(self.core.order['status'], 'paused')
        self.assertEqual(len(self.transport.sent), 1)

    def test_rejected_failed_canceled_and_bad_result_never_advance(self):
        for change in ({'status': 0}, {'status': 5}, {'status': 6}, {'success': False}, {'message': 'DONE'}):
            with self.subTest(change=change):
                self.setUp(); self.start()
                self.result(**change); self.core.tick(True)
                self.assertEqual(self.core.order['status'], 'failed')
                self.assertEqual(len(self.transport.sent), 1)
                self.assertEqual(self.core.order['stage'], 0)

    def test_no_ack_and_execution_timeout_request_stop_without_retry(self):
        for accepted in (False, True):
            self.setUp(); self.start()
            task_id = self.core.active['id']
            if accepted: self.core.event(task_id, 'accepted', {})
            self.now = 6; self.core.tick(True)
            self.assertEqual(self.core.order['status'], 'failed')
            self.assertEqual(self.transport.stops, ['M1'])
            self.core.event(task_id, 'accepted', {})  # a late goal response is stopped again
            self.assertEqual(self.transport.stops, ['M1', 'M1'])
            self.core.event(task_id, 'done', dict(status=4, success=True, message='IDLE'))
            self.core.tick(True)
            self.assertEqual(self.core.order['stage'], 0)
            self.assertEqual(len(self.transport.sent), 1)

    def test_device_disconnect_blocks_pipeline(self):
        self.start()
        self.transport.availability['M1'] = False
        self.now = 3; self.core.tick(True)
        self.assertEqual(self.core.order['status'], 'failed')
        self.assertEqual(self.transport.stops, ['M1'])

    def test_unready_and_invalid_orders_send_nothing(self):
        for quantity in (0, 3, True, '2'):
            self.core.command({'id': str(quantity), 'action': 'start', 'product_type': 'A', 'quantity': quantity})
        self.transport.availability['arm3'] = False
        self.core.tick(True)
        self.start()
        self.assertIsNone(self.core.order)
        self.assertEqual(self.transport.sent, [])

    def test_crash_journal_is_not_replayed(self):
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / 'order.json'
            self.core = ProcessController(self.transport, state_file=state)
            self.core.tick(True); self.start()
            saved = json.loads(state.read_text())
            self.assertEqual(saved['active']['command'], 'GO_TO_MAT')
            fresh = FakeTransport()
            recovered = ProcessController(fresh, state_file=state)
            recovered.tick(True)
            self.assertEqual(recovered.order['status'], 'failed')
            self.assertEqual(fresh.sent, [])
            self.assertEqual(fresh.stops, ['M1'])

    def test_old_order_and_old_result_are_ignored(self):
        self.start()
        self.core.command({'id': 'old-pause', 'action': 'pause', 'order_id': 'old'})
        self.core.event('old-task', 'done', dict(status=4, success=True, message='IDLE'))
        self.assertFalse(self.core.order['pause_requested'])
        self.assertEqual(self.core.order['stage'], 0)


if __name__ == '__main__': unittest.main()
