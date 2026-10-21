import json
from pathlib import Path
import queue
import tempfile
import unittest
from unittest.mock import Mock
from test_process import FakeTransport
from parallel_process import ParallelProcessController
from parked_preparation import execute


class ParkedPreparationTest(unittest.TestCase):
    def setUp(self):
        self.transport = FakeTransport()
        self.transport.prepare_parked = Mock()
        self.core = ParallelProcessController(self.transport)
        self.core.tick(True)

    def prepare(self, **changes):
        payload = dict(id='prepare', action='prepare_parked', device='M1',
                       order_id=None, recovery_revision=0, operator_confirmed=True)
        self.core.command(dict(payload, **changes))

    def test_offline_robot_can_be_prepared_and_reserves_entire_process(self):
        self.transport.availability = dict.fromkeys(self.core.ready, False)
        self.core.tick(True)
        self.assertTrue(self.core.can_prepare_parked())
        self.prepare()
        self.prepare(id='duplicate', device='M2', recovery_revision=1)
        self.core.command(dict(id='start', action='start', product_type='A', quantity=1))
        self.assertEqual(self.transport.prepare_parked.call_count, 1)
        self.assertFalse(self.core.can_prepare_parked())
        self.assertFalse(self.core.can_manual_move())
        self.assertIsNone(self.core.order)
        self.core.tick(False)  # ROS/web disconnect during setup must not replay.
        self.assertEqual(self.transport.stops, [])
        self.core.event(self.core.active['id'], 'done', dict(success=True, message='IDLE'))
        self.core.tick(True)
        self.assertTrue(self.core.can_prepare_parked())
        self.assertEqual(self.transport.sent, [])

    def test_invalid_or_stale_confirmation_sends_nothing(self):
        for i, patch in enumerate([dict(operator_confirmed=False), dict(device='arm1'),
                                   dict(order_id='old'), dict(recovery_revision=1),
                                   dict(recovery_revision=True)]):
            self.prepare(id=str(i), **patch)
        self.transport.prepare_parked.assert_not_called()

    def test_failed_and_running_orders_require_reset_first(self):
        for status in ('failed', 'running', 'paused', 'waiting'):
            self.core.order = dict(id='order', status=status)
            self.prepare(id=status, order_id='order')
        self.transport.prepare_parked.assert_not_called()

    def test_uncertain_result_and_restart_never_unlock_or_replay(self):
        with tempfile.TemporaryDirectory() as directory:
            self.core.state_file = Path(directory)/'state.json'
            self.prepare()
            self.core.event(self.core.active['id'], 'done',
                            dict(success=False, uncertain=True, message='SSH timeout'))
            self.assertFalse(self.core.can_prepare_parked())
            restored = ParallelProcessController(self.transport, state_file=self.core.state_file)
            restored.tick(True)
            self.assertFalse(restored.can_prepare_parked())
            self.assertEqual(self.transport.prepare_parked.call_count, 1)
            self.assertEqual(self.transport.stops, [])

    def test_worker_uses_exact_single_robot_cli_and_only_confirmed_success(self):
        for device in ('M1', 'M2'):
            events = queue.Queue()
            runner = Mock(return_value=Mock(returncode=0, stdout='ready'))
            execute(dict(id='request', device=device), events, runner=runner, root='/tmp/project')
            self.assertEqual(runner.call_args.args[0],
                             ['bash', '/tmp/project/start_amr.sh', '--ready', '--parked', '--robot', device])
            self.assertEqual(runner.call_args.kwargs['env']['HOST_AMR_BATCH'], '1')
            self.assertTrue(events.get()[2]['success'])
            runner.side_effect = [Mock(returncode=0, stdout='online'), Mock(returncode=1, stdout='lost')]
            execute(dict(id='request', device=device), events, runner=runner, root='/tmp/project')
            self.assertTrue(events.get()[2]['uncertain'])

    def test_unreachable_robot_does_not_start_preparation_or_leave_uncertain_work(self):
        events = queue.Queue()
        runner = Mock(return_value=Mock(returncode=1, stdout='connection refused'))
        execute(dict(id='request', device='M1'), events, runner=runner, root='/tmp/project')
        self.assertEqual(runner.call_count, 1)
        self.assertIn('--status', runner.call_args.args[0])
        self.assertFalse(events.get()[2]['uncertain'])

    def test_mock_mode_never_prepares_real_robot(self):
        self.core.mode = 'mock'
        self.prepare()
        self.transport.prepare_parked.assert_not_called()

if __name__ == '__main__':
    unittest.main()
