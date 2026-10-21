"""Initialization contracts with a fake transport: these tests cannot move hardware."""
import json
from pathlib import Path
import tempfile
import unittest
from test_process import FakeTransport
from full_reset import FullResetController
from initial_state import INITIAL_STEPS


class FullResetTests(unittest.TestCase):
    def test_manual_inspection_cannot_initialize_all_devices(self):
        self.setUp();self.core.manual_inspection=True
        self.assertFalse(self.core.can_full_reset())
        command=self.begin();self.assertIn(command['id'],self.core.rejected)
        self.core.tick(True);self.assertEqual(self.transport.sent,[])

    def setUp(self):
        self.now = 0
        self.transport = FakeTransport()
        self.core = FullResetController(self.transport, clock=lambda: self.now, goal_timeout=2)
        self.core.tick(True)

    def begin(self, **patch):
        command = dict(id='reset-'+str(len(self.core.processed)), action='full_reset',
                       operator_confirmed=True, order_id=(self.core.order or {}).get('id'),
                       recovery_revision=self.core.manual_revision)
        command.update(patch)
        self.core.command(command)
        return command

    def result(self, **patch):
        task = self.core.full_reset['task']
        self.core.event(task['id'], 'accepted', {})
        data = dict(status=4, success=True, message='IDLE')
        data.update(patch)
        self.core.event(task['id'], 'done', data)
        return task

    def test_serial_results_required_and_linear_extended_before_parking(self):
        self.begin()
        for index, (device, command, _, _) in enumerate(INITIAL_STEPS):
            self.core.tick(True)
            self.assertEqual(len(self.transport.sent), index+1)
            self.assertEqual((self.transport.sent[-1]['device'], self.transport.sent[-1]['command']),
                             (device, command))
            self.core.tick(True)
            self.assertEqual(len(self.transport.sent), index+1)
            self.assertFalse(self.core.snapshot()['can_start'])
            task = self.result()
            self.core.event(task['id'], 'done', dict(status=4, success=True, message='IDLE'))
            self.assertEqual(self.core.full_reset['step'], index+1)
        self.assertEqual([t['command'] for t in self.transport.sent][-5:],
                         ['HOME_A', 'RESET', 'BUILD_SLIDE', 'GO_TO_PARK', 'GO_TO_PARK'])
        self.assertEqual(self.core.full_reset['status'], 'done')
        self.assertTrue(self.core.snapshot()['can_start'])
        self.assertFalse(self.transport.stops)

    def test_failed_order_archived_only_after_last_result(self):
        with tempfile.TemporaryDirectory() as directory:
            self.core.state_file = Path(directory)/'order.json'
            self.core.command(dict(id='start', action='start', product_type='A', quantity=1))
            self.core.fail('test failure')
            self.assertEqual(self.core.order['status'], 'failed')
            self.begin()
            for index in range(len(INITIAL_STEPS)):
                self.assertIsNotNone(self.core.order)
                self.core.tick(True)
                self.result()
            self.assertIsNone(self.core.order)
            self.assertEqual(len(list((Path(directory)/'order-history').glob('*.json'))), 1)
            saved = json.loads(self.core.state_file.read_text())
            self.assertEqual(saved['full_reset']['status'], 'done')
            self.assertIsNone(saved['order'])

    def test_each_terminal_failure_prevents_later_steps(self):
        for failed in range(len(INITIAL_STEPS)):
            with self.subTest(step=failed):
                self.setUp(); self.begin()
                for _ in range(failed):
                    self.core.tick(True); self.result()
                self.core.tick(True)
                self.result(status=6, success=False, message='ERROR')
                self.core.tick(True)
                self.assertEqual(len(self.transport.sent), failed+1)
                self.assertEqual(self.core.full_reset['status'], 'failed')
                self.assertFalse(self.core.reset_busy())
                self.assertTrue(self.core.can_full_reset())
                self.assertFalse(self.core.snapshot()['can_start'])
                self.core.command(dict(id='blocked-order', action='start', product_type='A', quantity=1))
                self.assertIn('blocked-order', self.core.rejected)

    def test_confirmation_and_stale_context_rejected(self):
        for patch in ({'operator_confirmed':False}, {'order_id':'old'},
                      {'recovery_revision':-1}, {'recovery_revision':True}):
            with self.subTest(patch=patch):
                self.setUp(); command = self.begin(**patch)
                self.assertIn(command['id'], self.core.rejected)
                self.assertIsNone(self.core.full_reset)
                self.assertFalse(self.transport.sent)

    def test_busy_order_and_unknown_work_block_initialization(self):
        self.core.command(dict(id='start', action='start', product_type='A', quantity=1))
        self.assertFalse(self.core.can_full_reset())
        self.begin()
        self.assertIsNone(self.core.full_reset)
        self.setUp(); self.core.unconfirmed.add('M1')
        self.assertFalse(self.core.can_full_reset())
        self.setUp(); self.core.recovery_uncertain = True
        self.assertFalse(self.core.can_full_reset())

    def test_duplicate_and_production_commands_cannot_overlap(self):
        command = self.begin()
        self.core.command(command)
        self.core.command(dict(id='start', action='start', product_type='A', quantity=1))
        self.core.tick(True)
        self.assertEqual(len(self.transport.sent), 1)
        self.assertIn('start', self.core.rejected)
        self.assertIsNone(self.core.order)
        self.assertFalse(self.core.can_prepare_parked())
        self.assertFalse(self.core.can_reset())

    def test_timeout_stays_locked_even_after_stop_ack_and_late_result_never_advances(self):
        self.begin(); self.core.tick(True)
        task = self.core.full_reset['task'].copy()
        self.now = 3; self.core.tick(True)
        self.assertTrue(self.core.full_reset['uncertain'])
        self.assertEqual(self.transport.stops, ['arm1'])
        self.core.event(None, 'stop', dict(status=4, success=True, message='IDLE'))
        self.assertTrue(self.core.reset_busy())
        self.core.event(task['id'], 'accepted', {})
        self.assertEqual(self.transport.stops, ['arm1', 'arm1'])
        self.core.event(task['id'], 'done', dict(status=4, success=True, message='IDLE'))
        self.core.tick(True)
        self.assertEqual(len(self.transport.sent), 1)
        self.assertEqual(self.core.full_reset['step'], 0)
        self.assertFalse(self.core.reset_busy())

    def test_cancel_and_disconnect_stop_current_without_next_motion(self):
        for reason in ('cancel', 'disconnect', 'feedback'):
            with self.subTest(reason=reason):
                self.setUp(); self.begin(); self.core.tick(True)
                if reason == 'cancel':
                    self.core.command(dict(id='cancel', action='cancel_full_reset',
                                           reset_id=self.core.full_reset['id']))
                elif reason == 'disconnect': self.core.tick(False)
                else: self.core.event(self.core.full_reset['task']['id'], 'feedback', {'message':'ERROR'})
                self.assertTrue(self.core.reset_busy())
                self.result()
                self.core.tick(True)
                self.assertEqual(self.core.full_reset['status'], 'failed')
                self.assertEqual(len(self.transport.sent), 1)

    def test_restart_retains_uncertain_task_and_never_replays(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'order.json'
            self.core.state_file = path
            self.begin(); self.core.tick(True)
            transport = FakeTransport()
            restored = FullResetController(transport, state_file=path)
            restored.tick(True)
            self.assertFalse(transport.sent)
            self.assertTrue(restored.reset_busy())
            self.assertEqual(restored.full_reset['status'], 'failed')
            self.assertFalse(restored.snapshot()['can_start'])

    def test_unknown_result_keeps_reservation(self):
        self.begin(); self.core.tick(True)
        self.result(uncertain=True, success=False, status=0)
        self.assertTrue(self.core.reset_busy())
        self.core.tick(True)
        self.assertEqual(len(self.transport.sent), 1)
    def test_unknown_ros_status_after_acceptance_is_not_terminal(self):
        self.begin(); self.core.tick(True)
        self.result(success=False, status=0)
        self.assertTrue(self.core.full_reset['uncertain'])
        self.assertTrue(self.core.reset_busy())
    def test_original_completion_does_not_overtake_pending_stop(self):
        self.transport.stop = lambda device: 'stop-1'
        self.begin(); self.core.tick(True)
        self.core.abort_full_reset('cancel')
        self.result(status=5, success=False, message='ERROR')
        self.assertTrue(self.core.reset_busy())
        self.assertFalse(self.core.can_full_reset())
        self.core.event('other-stop', 'stop', dict(device='arm1', status=4, success=True, message='IDLE'))
        self.assertTrue(self.core.reset_busy())
        self.core.event('stop-1', 'stop', dict(status=4, success=True, message='IDLE'))
        self.assertFalse(self.core.reset_busy())
    def test_rejected_stop_after_terminal_home_error_unlocks_recovery_not_new_order(self):
        self.transport.stop = lambda device: 'stop-1'
        self.begin(); self.core.tick(True)
        self.core.event(self.core.full_reset['task']['id'],'feedback',{'message':'ERROR'})
        self.result(status=6,success=False,message='ERROR')
        self.assertTrue(self.core.reset_busy())
        self.core.event('stop-1','stop',dict(status=0,success=False,message='Goal 거절',rejected=True))
        self.assertFalse(self.core.reset_busy())
        self.assertTrue(self.core.can_full_reset())
        self.assertFalse(self.core.snapshot()['can_start'])
        self.assertEqual(self.core.snapshot()['devices']['warehouse']['state'],'failed')
    def test_rejected_stop_before_original_result_keeps_motion_locked(self):
        self.transport.stop = lambda device: 'stop-1'
        self.begin(); self.core.tick(True)
        task=self.core.full_reset['task']
        self.core.event(task['id'],'accepted',{})
        self.core.abort_full_reset('error')
        self.core.event('stop-1','stop',dict(status=0,success=False,message='Goal 거절',rejected=True))
        self.assertTrue(self.core.reset_busy())
        self.core.event(task['id'],'done',dict(status=6,success=False,message='ERROR'))
        self.assertFalse(self.core.reset_busy())
    def test_unknown_stop_result_does_not_unlock(self):
        self.transport.stop = lambda device: 'stop-1'
        self.begin(); self.core.tick(True);self.core.abort_full_reset('error')
        self.result(status=6,success=False,message='ERROR')
        for data in (dict(status=0,success=False,message='UNKNOWN'),
                     dict(status=0,success=False,message='lost',uncertain=True,rejected=True)):
            self.core.event('stop-1','stop',data)
            self.assertTrue(self.core.reset_busy())

    def test_rejected_goal_allows_explicit_fresh_restart(self):
        self.begin(); self.core.tick(True)
        task = self.core.full_reset['task']
        self.core.event(task['id'], 'done', dict(status=0, success=False, message='Goal 거절'))
        self.assertFalse(self.core.reset_busy())
        self.begin(); self.core.tick(True)
        self.assertEqual(len(self.transport.sent), 2)
        self.assertEqual(self.core.full_reset['step'], 0)

    def test_confirmed_parking_prepares_nav_before_arms_without_driving(self):
        prepared=[]
        self.transport.prepare_parked=lambda task:prepared.append(task)
        self.begin(amrs_parked=True)
        for index in range(7):
            self.core.tick(True)
            task=self.core.full_reset['task']
            if task.get('preparation'):
                self.assertEqual(task['command'],'PREPARE_PARKED')
                self.transport.availability[task['device']]=False
                self.core.tick(True)  # Expected discovery gap while Nav2 resets.
                self.assertEqual(self.core.full_reset['status'],'running')
                self.transport.availability[task['device']]=True
                self.core.event(task['id'],'done',dict(success=True,message='IDLE',uncertain=False))
            else:self.result()
        self.assertEqual([t['device'] for t in prepared],['M1','M2'])
        self.assertEqual([(t['device'],t['command']) for t in self.transport.sent],
                         [('arm1','CLEAR_ERROR'),('arm2','CLEAR_ERROR'),('arm1','HOME_A'),
                          ('arm2','RESET'),('arm2','BUILD_SLIDE')])
        self.assertEqual(self.core.full_reset['status'],'done')
        self.assertEqual(self.core.snapshot()['full_reset']['total'],7)

    def test_parked_worker_failure_reserves_robot_and_does_not_move_arms(self):
        self.transport.prepare_parked=lambda task:None
        self.begin(amrs_parked=True)
        for _ in range(2):self.core.tick(True);self.result()
        self.core.tick(True);task=self.core.full_reset['task']
        self.core.event(task['id'],'done',dict(success=False,uncertain=True,message='SSH disconnected'))
        self.core.tick(True)
        self.assertTrue(self.core.reset_busy())
        self.assertFalse(self.transport.stops)
        self.assertEqual(len(self.transport.sent),2)

    def test_parked_worker_cancel_waits_for_result_without_stop_or_further_motion(self):
        self.transport.prepare_parked=lambda task:None
        self.begin(amrs_parked=True)
        for _ in range(2):self.core.tick(True);self.result()
        self.core.tick(True);task=self.core.full_reset['task']
        self.core.abort_full_reset('cancel')
        self.assertTrue(self.core.reset_busy())
        self.assertFalse(self.transport.stops)
        self.core.event(task['id'],'done',dict(success=True,message='IDLE'))
        self.core.tick(True)
        self.assertFalse(self.core.reset_busy())
        self.assertEqual(self.core.full_reset['status'],'failed')
        self.assertEqual(len(self.transport.sent),2)

    def test_parked_option_requires_boolean_and_hardware_mode(self):
        for flag in ('true',1,None):
            self.setUp();c=self.begin(amrs_parked=flag)
            self.assertIn(c['id'],self.core.rejected)
        self.setUp();self.core.mode='mock'
        c=self.begin(amrs_parked=True)
        self.assertIn(c['id'],self.core.rejected)
