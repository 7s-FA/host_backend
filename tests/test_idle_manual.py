"""Manual moves without an order stay exclusive, confirmed, and never replayed."""
import json
from pathlib import Path
import tempfile
import unittest
from test_process import ProcessTest, ProcessController, FakeTransport


class IdleManualTest(unittest.TestCase):
    setUp = ProcessTest.setUp
    result = ProcessTest.result

    def test_normal_mode_retains_all_device_requirement(self):
        self.core.ready['M1']=False
        self.assertFalse(self.core.can_manual_move('M2'))

    def test_inspection_mode_never_starts_production_even_when_all_ready(self):
        self.core.manual_inspection=True
        self.assertTrue(self.core.can_manual_move('M2'))
        self.assertFalse(self.core.snapshot()['can_start'])
        self.assertTrue(self.core.snapshot()['manual_inspection'])
        self.core.command(dict(id='production',action='start',product_type='A',quantity=1))
        self.assertIn('production',self.core.rejected)
        self.assertIsNone(self.core.order)
        self.assertEqual(self.transport.sent,[])

    def test_only_selected_robot_required_without_order(self):
        self.core.manual_inspection=True
        self.core.ready.update(M1=False,arm1=False,arm2=False,arm3=False,M2=True)
        self.assertEqual(self.core.snapshot()['manual_move_available'],{'M1':False,'M2':True})
        self.assertFalse(self.core.snapshot()['can_start'])
        payload=dict(action='manual_move',order_id=None,stage=0,recovery_revision=0,
                     operator_confirmed=True,destination='GO_TO_MAT')
        self.core.command(dict(payload,id='offline',device='M1'))
        self.assertEqual(self.transport.sent,[])
        self.core.command(dict(payload,id='online',device='M2'))
        self.assertEqual([t['device'] for t in self.transport.sent],['M2'])
        self.assertFalse(self.core.can_manual_move())

    def test_other_robot_offline_never_bypasses_pending_operations(self):
        self.core.manual_inspection=True
        self.core.ready['M1']=False
        self.assertTrue(self.core.can_manual_move('M2'))
        self.core.recovery_uncertain=True
        self.assertFalse(self.core.can_manual_move('M2'))
        self.core.recovery_uncertain=False;self.core.link=False
        self.assertFalse(self.core.can_manual_move('M2'))

    def move(self, **extra):
        self.core.command(dict(id='manual-'+str(len(self.core.processed)), action='manual_move',
                               order_id=None, stage=0, recovery_revision=self.core.manual_revision,
                               operator_confirmed=True, device='M1', destination='GO_TO_MAT', **extra))

    def test_no_order_all_destinations_and_robots(self):
        for device in ('M1', 'M2'):
            for dest in ('GO_TO_MAT', 'GO_TO_ASM', 'GO_TO_PARK', 'GO_TO_REST'):
                self.assertTrue(self.core.snapshot()['can_manual_move'])
                self.core.command(dict(id=str(len(self.core.processed)), action='manual_move',
                                       order_id=None, stage=0, recovery_revision=self.core.manual_revision,
                                       operator_confirmed=True, device=device, destination=dest))
                self.assertEqual((self.core.active['device'],self.core.active['command']), (device,dest))
                self.assertIsNone(self.core.order)
                self.assertFalse(self.core.snapshot()['can_start'])
                self.assertFalse(self.core.snapshot()['can_manual_move'])
                self.result();self.core.tick(True)
                self.assertIsNone(self.core.order)
                self.assertIsNone(self.core.active)
        self.assertEqual(len(self.transport.sent), 8)

    def test_active_move_blocks_order_and_second_move(self):
        self.move();self.move()
        self.core.command(dict(id='start',action='start',product_type='A',quantity=1))
        self.assertEqual(len(self.transport.sent), 1)
        self.assertIsNone(self.core.order)

    def test_stale_dialog_rejected_after_move_finishes(self):
        self.move();self.result()
        self.core.command(dict(id='stale',action='manual_move',order_id=None,stage=0,
                               recovery_revision=0,operator_confirmed=True,device='M2',destination='GO_TO_PARK'))
        self.assertEqual(len(self.transport.sent), 1)

    def test_unconfirmed_wrong_order_and_invalid_target_send_nothing(self):
        payload=dict(action='manual_move',order_id=None,stage=0,recovery_revision=0,
                     operator_confirmed=True,device='M1',destination='GO_TO_MAT')
        for i,patch in enumerate([dict(operator_confirmed=False),dict(order_id='old'),dict(stage=1),
                                  dict(destination='RESTART'),dict(device='arm1')]):
            self.core.command(dict(payload, id=str(i), **patch))
        self.assertEqual(self.transport.sent, [])
        self.assertEqual(self.core.manual_revision, 0)

    def test_timeout_never_unlocks_on_timer(self):
        self.move();self.now=3;self.core.tick(True)
        self.assertEqual(self.transport.stops, ['M1'])
        self.assertFalse(self.core.can_manual_move())
        self.core.event(None,'stop',dict(device='M1',status=4,success=True,message='IDLE'))
        self.assertFalse(self.core.can_manual_move())  # original action still outstanding
        self.result(status=6,success=False,message='ERROR')
        self.core.event(None,'stop',dict(device='M1',status=4,success=True,message='IDLE'))
        self.assertTrue(self.core.can_manual_move())

    def test_restart_without_order_stops_saved_manual_and_never_replays(self):
        with tempfile.TemporaryDirectory() as directory:
            self.core.state_file=Path(directory)/'order.json'
            self.move()
            transport=FakeTransport()
            restored=ProcessController(transport,state_file=self.core.state_file)
            restored.tick(True)
            self.assertEqual(transport.sent, [])
            self.assertEqual(transport.stops, ['M1'])
            self.assertFalse(restored.snapshot()['can_start'])
            self.assertFalse(restored.can_manual_move())
            restored.event(None,'stop',dict(device='M1',status=4,success=True,message='IDLE'))
            self.assertTrue(restored.can_manual_move())

    def test_done_order_is_preserved(self):
        ProcessTest.start(self)
        while self.core.order['status'] != 'done':
            self.result();self.core.tick(True)
        before=self.core.order.copy()
        self.core.command(dict(id='after-done',action='manual_move',order_id=before['id'],
                               stage=before['stage'],recovery_revision=0,operator_confirmed=True,
                               device='M2',destination='GO_TO_PARK'))
        self.result();self.core.tick(True)
        for key in ('id','status','stage','completed','quantity','transport_remaining','product_remaining'):
            self.assertEqual(self.core.order[key],before[key])


if __name__ == '__main__':
    unittest.main()
