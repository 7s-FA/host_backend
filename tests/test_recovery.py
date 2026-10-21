"""Failure recovery never replays completed work or changes counts on manual moves."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_process as base
from test_process import FakeTransport
from control import ProcessController

class RecoveryTest(unittest.TestCase):
    setUp = base.ProcessTest.setUp
    start = base.ProcessTest.start
    result = base.ProcessTest.result
    command = base.ProcessTest.command
    def recover(self, action='retry', **extra):
        self.command(action, stage=self.core.order['stage'],
                     recovery_revision=self.core.order.get('recovery_revision', 0),
                     operator_confirmed=True, **extra)

    def failed_load(self, automatic=True, quantity=1):
        self.start(automatic=automatic, quantity=quantity)
        while self.core.active['device'] != 'arm3':
            self.result()
            if self.core.order['status']=='waiting':
                self.command('next',stage=self.core.order['stage'])
            self.core.tick(True)
        old=self.result(status=6,success=False,message='ERROR')
        return old

    def test_retry_load_preserves_mode_counts_and_result_gating(self):
        for automatic in (True, False):
            with self.subTest(automatic=automatic):
                self.setUp()
                old=self.failed_load(automatic);before=self.core.order.copy();count=len(self.transport.sent)
                self.recover();self.core.tick(True)
                task=self.core.active.copy()
                self.assertEqual((task['device'],task['command']),('arm3','LOAD_A'))
                self.assertNotEqual(task['id'],old['id'])
                self.assertEqual(self.core.order['auto_advance'],automatic)
                self.core.event(old['id'],'done',dict(status=4,success=True,message='IDLE'))
                self.core.event(task['id'],'feedback',{'message':'IDLE'})
                self.core.tick(True)
                self.assertEqual(self.core.order['completed'],before['completed'])
                self.assertEqual(len(self.transport.sent),count+1)
                self.result();self.core.tick(True)
                self.assertEqual(self.core.order['completed'],1)
                self.assertEqual(self.core.order['transport_remaining'],0)
                self.assertEqual(self.core.order['status'],'running' if automatic else 'waiting')
                self.assertEqual(len(self.transport.sent),count+(2 if automatic else 1))
                if not automatic:
                    self.command('next',stage=5);self.core.tick(True)
                self.assertEqual(self.core.active['command'],'GO_TO_PARK')

    def test_automatic_two_product_retry_completes_remaining_plan_once(self):
        self.failed_load(quantity=2)
        self.recover();self.core.tick(True);self.result();self.core.tick(True)
        self.assertEqual((self.core.active['device'], self.core.active['command']), ('M1', 'GO_TO_REST'))
        while self.core.order['status'] != 'done':
            self.result();self.core.tick(True)
        self.assertEqual((self.core.order['completed'], self.core.order['product_remaining'],
                          self.core.order['transport_remaining']), (2, 0, 0))
        commands=[(task['device'], task['command']) for task in self.transport.sent]
        self.assertEqual(commands.count(('arm2', 'BUILD_A')), 2)
        self.assertEqual(commands.count(('arm3', 'LOAD_A')), 3) # failed attempt + two successes
        self.assertEqual(commands[-1], ('M2', 'GO_TO_PARK'))

    def test_retry_failure_keeps_auto_mode_without_advancing(self):
        self.failed_load()
        for _ in range(2):
            self.recover();self.core.tick(True)
            self.assertEqual(self.core.active['command'],'LOAD_A')
            self.result(status=6,success=False,message='ERROR');self.core.tick(True)
            self.assertTrue(self.core.order['auto_advance'])
            self.assertEqual(self.core.order['status'],'failed')
            self.assertEqual(self.core.order['stage'],4)
            self.assertEqual(self.core.order['completed'],0)
        self.assertNotIn('GO_TO_PARK',[task['command'] for task in self.transport.sent])

    def test_transport_acceptance_retry_never_decrements_twice(self):
        self.start()
        while self.core.active['command']!='GO_TO_ASM':
            self.result();self.core.tick(True)
        self.result(status=6,success=False,message='ERROR')
        self.assertEqual(self.core.order['transport_remaining'],0)
        self.recover();self.core.tick(True);self.result()
        self.assertEqual(self.core.order['transport_remaining'],0)

    def test_recovery_rejects_active_uncertain_offline_and_unconfirmed(self):
        self.start();self.core.fail('uncertain',uncertain=True)
        self.assertFalse(self.core.can_recover());self.recover();self.assertEqual(len(self.transport.sent),1)
        self.core.event(self.core.active['id'],'done',dict(status=6,success=False,message='ERROR'))
        self.assertFalse(self.core.can_recover()) # stop outstanding
        self.core.event(None,'stop',dict(device='M1',status=6,success=False,message='ERROR'))
        self.assertTrue(self.core.can_recover()) # terminal result, operator must confirm
        self.command('retry',stage=0,recovery_revision=0,operator_confirmed=False)
        self.assertEqual(self.core.order['status'],'failed')
        self.core.tick(False);self.assertFalse(self.core.can_recover())

    def test_manual_all_destinations_preserve_order_and_are_exclusive(self):
        self.failed_load()
        for device in ('M1','M2'):
            for destination in ('GO_TO_MAT','GO_TO_ASM','GO_TO_REST','GO_TO_PARK'):
                before=self.core.order.copy();count=len(self.transport.sent)
                stale=dict(id='stale-'+str(count),action='retry',order_id=before['id'],stage=before['stage'],
                           recovery_revision=before.get('recovery_revision',0),operator_confirmed=True)
                self.recover('manual_move',device=device,destination=destination)
                self.assertFalse(self.core.can_recover());self.assertFalse(self.core.can_reset())
                self.recover();self.recover('manual_move',device='M2',destination='GO_TO_PARK')
                self.assertEqual(len(self.transport.sent),count+1)
                self.result();self.core.tick(True)
                for key in ('id','stage','completed','product_remaining','transport_remaining','status'):
                    self.assertEqual(self.core.order[key],before[key])
                self.assertTrue(self.core.can_recover())
                self.core.command(stale);self.core.tick(True)
                self.assertEqual(len(self.transport.sent),count+1)

    def test_invalid_manual_destination_and_duplicate_ids(self):
        self.failed_load()
        for device,destination in (('arm3','LOAD_A'),('M1','RESTART'),('M2','CUSTOM')):
            self.recover('manual_move',device=device,destination=destination)
            self.assertIsNone(self.core.active)
        cmd=dict(id='unique',action='manual_move',order_id=self.core.order['id'],stage=4,
                 recovery_revision=0,operator_confirmed=True,device='M1',destination='GO_TO_PARK')
        count=len(self.transport.sent)
        self.core.command(cmd);self.core.command(cmd)
        self.assertEqual(len(self.transport.sent),count+1)
        self.result();self.core.command(cmd);self.assertEqual(len(self.transport.sent),count+1)

    def test_manual_timeout_never_allows_second_move_before_terminal(self):
        self.failed_load();self.recover('manual_move',device='M1',destination='GO_TO_PARK')
        old=self.core.active.copy();self.now+=3;self.core.tick(True)
        self.assertEqual(self.transport.stops,['M1']);self.assertFalse(self.core.can_recover())
        self.core.event(old['id'],'accepted',{});self.assertEqual(self.transport.stops,['M1','M1'])
        self.core.event(None,'stop',dict(device='M1',status=6,success=False,message='ERROR'))
        self.assertFalse(self.core.can_recover())
        self.core.event(old['id'],'done',dict(status=4,success=True,message='IDLE'))
        self.assertTrue(self.core.can_recover());self.assertEqual(self.core.order['stage'],4)

    def test_manual_restart_never_replays_movement(self):
        with tempfile.TemporaryDirectory() as folder:
            self.core.state_file=Path(folder)/'state.json'
            self.failed_load();self.recover('manual_move',device='M2',destination='GO_TO_REST')
            transport=FakeTransport();recovered=ProcessController(transport,state_file=self.core.state_file)
            recovered.tick(True)
            self.assertEqual(transport.sent,[]);self.assertEqual(transport.stops,['M2'])
            self.assertFalse(recovered.can_recover())
            recovered.event(None,'stop',dict(device='M2',status=4,success=True,message='IDLE'))
            self.assertTrue(recovered.can_recover());self.assertEqual(recovered.order['stage'],4)

if __name__=='__main__':unittest.main()
