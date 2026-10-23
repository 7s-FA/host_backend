import json
from pathlib import Path
import tempfile
import unittest
from test_parallel_process import CorrelatedTransport, OK
from queued_process import QueuedProcessController


class QueueTest(unittest.TestCase):
    def setUp(self):
        self.transport = CorrelatedTransport()
        self.core = QueuedProcessController(self.transport)
        self.core.tick(True)

    def command(self, action, **extra):
        command = dict(id=str(len(self.core.processed)), action=action, **extra)
        self.core.command(command)
        return command

    def finish(self):
        for _ in range(30):
            self.core.tick(True)
            for task in list(self.core.inflight.values()):
                self.core.event(task['id'], 'accepted', {})
                self.core.event(task['id'], 'done', OK)
            if self.core.order['status'] == 'done':
                return
        self.fail('batch did not complete')

    def test_all_product_combinations_and_commands(self):
        for a, b in ((1, 0), (0, 1), (2, 0), (0, 2), (1, 1), (2, 1), (1, 2), (2, 2)):
            self.setUp()
            self.command('start', quantities={'A': a, 'B': b})
            products = self.core.order['products']
            self.assertEqual(products, (['A']*a+['B']*b)[:2])
            for step in self.core.plan:
                if step.device.startswith('arm') and step.product_no:
                    self.assertTrue(step.command.endswith('_'+products[step.product_no-1]))
            self.finish()
            self.assertEqual(self.core.order['completed'], len(products))
            n = len(self.transport.sent)
            for _ in range(3): self.core.tick(True)
            self.assertEqual(len(self.transport.sent), n, 'never auto-start another pallet')

    def test_append_while_running_is_fifo_and_deduplicated(self):
        self.command('start', quantities={'A': 2, 'B': 2})
        self.core.tick(True)
        before = self.core.order.copy()
        cmd = self.command('enqueue', quantities={'A': 1, 'B': 1})
        self.core.command(cmd)
        self.assertEqual(self.core.order, before)
        self.assertEqual([b['products'] for b in self.core.pending_batches], [['B','B'], ['A','B']])
        self.finish()
        snapshot = self.core.snapshot()
        self.assertTrue(snapshot['can_next_batch'])
        self.command('next_batch', order_id=self.core.order['id'], queue_revision=snapshot['queue_revision'], operator_confirmed=False)
        self.assertEqual(self.core.order['status'], 'done')
        self.command('next_batch', order_id=self.core.order['id'], queue_revision=snapshot['queue_revision'], operator_confirmed=True)
        self.assertEqual(self.core.order['products'], ['B','B'])
        self.finish()
        self.assertEqual(self.core.order['completed'], 2)

    def test_restart_retains_queue_but_never_replays(self):
        with tempfile.TemporaryDirectory() as directory:
            self.core.state_file = Path(directory)/'order.json'
            self.command('start', quantities={'A': 1, 'B': 1})
            self.core.tick(True)
            self.command('enqueue', quantities={'A': 2, 'B': 2})
            restored = QueuedProcessController(self.transport, state_file=self.core.state_file)
            self.assertEqual(restored.order['status'], 'failed')
            self.assertEqual(restored.order['products'], ['A','B'])
            self.assertEqual(len(restored.pending_batches), 2)
            self.assertFalse(restored.snapshot()['can_next_batch'])
            self.assertEqual(restored.plan[11].command, 'BUILD_LOAD_B')

    def test_invalid_and_capacity_limits(self):
        for quantities in ({'A':True,'B':0}, {'A':3,'B':0}, {'A':0,'B':0}, {'A':1}, {'A':1,'B':1,'C':1}):
            self.command('enqueue', quantities=quantities)
        self.assertEqual(self.core.pending_batches, [])
        for _ in range(9): self.command('enqueue', quantities={'A':2,'B':2})
        self.assertEqual(sum(len(b['products']) for b in self.core.pending_batches), 32)

    def test_failed_batch_does_not_start_pending_and_clear_preserves_current(self):
        self.command('start', quantities={'A':2,'B':2})
        self.core.order['status'] = 'failed'
        self.command('next_batch', order_id=self.core.order['id'], queue_revision=self.core.queue_revision, operator_confirmed=True)
        self.assertEqual(self.core.order['status'], 'failed')
        self.command('clear_queue', order_id=self.core.order['id'], queue_revision=self.core.queue_revision, operator_confirmed=True)
        self.assertEqual(self.core.pending_batches, [])
        self.assertEqual(self.core.order['status'], 'failed')


class MovementResetTest(unittest.TestCase):
    def setUp(self):
        self.now = 0
        self.transport = CorrelatedTransport()
        self.core = QueuedProcessController(self.transport, clock=lambda:self.now)
        self.core.tick(True)
        self.core.active = dict(id='old', manual=True, standalone=True, failed=True,
                                device='M2', command='GO_TO_PARK', label='old', accepted=True)
        self.core.recovery_uncertain = True
        self.core.reset_stop_device = 'M2'

    def reset(self, **extra):
        self.core.command(dict(id='reset', action='reset_movement', device='M2', order_id=None,
                               recovery_revision=self.core.manual_revision, operator_confirmed=True, **extra))

    def test_power_loss_cleanup_waits_for_both_results_and_never_moves(self):
        self.assertTrue(self.core.can_reset_movement('M2'))
        self.assertFalse(self.core.can_reset_movement('M1'))
        self.reset()
        self.assertEqual(self.transport.sent, [])
        self.core.event('wrong', 'stop', dict(OK, device='M2'))
        self.assertEqual(self.transport.sent, [])
        self.core.event('stop-1', 'stop', dict(OK, device='M2'))
        self.assertEqual([t['command'] for t in self.transport.sent], ['RESTART'])
        self.core.event('old', 'done', OK)
        self.assertIsNotNone(self.core.active)
        self.core.event(self.core.active['id'], 'done', OK)
        self.assertIsNone(self.core.active)
        self.assertFalse(self.core.recovery_uncertain)
        self.assertTrue(self.core.can_manual_move('M2'))

    def test_rejection_timeout_and_restart_preserve_lock(self):
        with tempfile.TemporaryDirectory() as directory:
            self.core.state_file = Path(directory)/'order.json'
            self.reset()
            restored = QueuedProcessController(self.transport, state_file=self.core.state_file)
            self.assertTrue(restored.active['failed'])
            self.assertTrue(restored.recovery_uncertain)
            self.assertFalse(restored.can_manual_move('M2'))
            self.now = 16
            self.core.tick(True)
            self.core.event('stop-1', 'stop', dict(OK, device='M2'))
            self.assertEqual(self.transport.sent, [])

    def test_running_robot_and_active_production_cannot_be_reset(self):
        self.core.active['failed'] = False
        self.assertFalse(self.core.can_reset_movement('M2'))
        self.core.active['failed'] = True
        self.core.order = dict(status='running')
        self.assertFalse(self.core.can_reset_movement('M2'))
