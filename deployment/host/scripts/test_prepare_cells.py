import importlib.util
from pathlib import Path
import unittest
from unittest.mock import Mock,patch
import tempfile,json

spec=importlib.util.spec_from_file_location('prepare_cells',Path(__file__).with_name('prepare_cells.py'))
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)


class PreparationTests(unittest.TestCase):
    def test_cleanup_only_never_homes_or_enables_amr_torque(self):
        calls=[];verify=Mock();report=Mock()
        module.cleanup_only(lambda *args:calls.append(args[:2]),verify,report)
        self.assertEqual(calls,[('/arm1/data','CLEAR_ERROR'),('/arm2/data','CLEAR_ERROR'),('/M1/data','RESTART'),('/M2/data','RESTART')])
        verify.assert_called_once()
        self.assertIn('전체 작업 정리 완료',report.call_args.args[0])

    def test_cleanup_failure_reports_incomplete_but_checks_other_devices(self):
        send=Mock(side_effect=[RuntimeError('hardware cleanup unconfirmed'),None,None,None])
        report=Mock();verify=Mock()
        with self.assertRaisesRegex(RuntimeError,'전체 정리 미완료'):
            module.cleanup_only(send,verify,report)
        self.assertEqual(send.call_count,4)
        verify.assert_called_once()
        self.assertFalse(any('전체 작업 정리 완료' in c.args[0] for c in report.call_args_list))

    def test_cleanup_postcheck_failure_is_not_success(self):
        with self.assertRaisesRegex(RuntimeError,'리니어'):
            module.cleanup_only(Mock(),Mock(side_effect=RuntimeError('리니어 정지 미확인')),Mock())

    def test_cleanup_preserves_unresolved_records_without_remote_commands(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'order.json'
            for saved in ({'order':{'status':'failed'}},{'full_reset':{'status':'failed','stop_id':'pending-stop'}},{'active':{'device':'M1'}}):
                path.write_text(json.dumps(saved))
                with patch.dict(module.os.environ,ROS_DOMAIN_ID='40',HOST_MOCK='0',HOST_STATE_FILE=str(path)),patch.object(module.subprocess,'run') as remote:
                    with self.assertRaisesRegex(RuntimeError,'미정리'):module.main(cleanup=True)
                    remote.assert_not_called()
                    self.assertEqual(json.loads(path.read_text()),saved)

    def test_amr_readiness_does_not_reseed_pose_and_propagates_failure(self):
        with patch.object(module.subprocess,'run') as run:
            module.prepare_amrs()
            self.assertEqual(run.call_args.args[0][-1],'--ready')
            self.assertNotIn('--parked',run.call_args.args[0])
            run.side_effect=module.subprocess.CalledProcessError(1,'host-ready')
            with self.assertRaises(module.subprocess.CalledProcessError):
                module.prepare_amrs()
    def test_order_state_and_unfinished_parallel_work_block_motion(self):
        for state in ({'order':{'status':'failed'}},{'order':{'status':'running'}},
                      {'active':{'manual':True}},{'recovery_uncertain':True},
                      {'parallel_state':{'orphans':{'x':{}}}},
                      {'parallel_state':{'unconfirmed':['M2']}}):
            self.assertTrue(module.unresolved(state),state)
        self.assertFalse(module.unresolved({}))
        self.assertFalse(module.unresolved({'order':{'status':'completed'}}))
    def test_goal_failure_prevents_later_motion(self):
        # Each cleanup/unlock may reject a running job, stale odometry, or a
        # hardware failure. None of these failures may fall through to HOME.
        for failed_index in range(4):
            send=Mock(side_effect=[None]*failed_index+[RuntimeError('not stationary')])
            verify=Mock()
            with self.subTest(failed_index=failed_index),self.assertRaises(RuntimeError):
                module.prepare(send,verify)
            self.assertEqual(send.call_count,failed_index+1)
            verify.assert_not_called()
            self.assertFalse(any(c.args[1] in ('HOME_A','PREPARE_HOME') for c in send.call_args_list))
    def test_all_releases_and_readiness_checks_precede_home(self):
        calls=[]
        module.prepare(lambda *args:calls.append(args[:2]),lambda:calls.append(('verify',)))
        self.assertEqual(calls,[
            ('/arm1/data','CLEAR_ERROR'),('/arm2/data','CLEAR_ERROR'),
            ('/M1/data','RESTART'),('/M2/data','RESTART'),('verify',),
            ('/arm1/data','HOME_A'),('/arm2/data','RESET'),('/arm2/data','BUILD_SLIDE'),
            ('/M1/data','GO_TO_PARK'),('/M2/data','GO_TO_PARK')])
    def test_readiness_failure_prevents_all_home_motion(self):
        send=Mock()
        with self.assertRaises(RuntimeError):
            module.prepare(send,Mock(side_effect=RuntimeError('linear moving')))
        self.assertEqual(send.call_count,4)
    def test_arm_home_failure_prevents_linear_preparation(self):
        send=Mock(side_effect=[None]*4+[RuntimeError('home failed')])
        verify=Mock()
        with self.assertRaises(RuntimeError):module.prepare(send,verify)
        verify.assert_called_once()
        self.assertEqual(send.call_count,5)
    def test_every_motion_failure_blocks_later_devices(self):
        for failed in range(4,9):
            send=Mock(side_effect=[None]*failed+[RuntimeError('motion failed')])
            with self.subTest(step=failed),self.assertRaises(RuntimeError):
                module.prepare(send,Mock())
            self.assertEqual(send.call_count,failed+1)
    def test_interrupted_full_reset_prevents_startup_replay(self):
        for job in ({'status':'running'},{'status':'failed','uncertain':True},
                    {'status':'failed','task':{'device':'M1'}}):
            self.assertTrue(module.unresolved({'full_reset':job}))
        self.assertFalse(module.unresolved({'order':{'status':'done'},'full_reset':{'status':'done'}}))
    def test_startup_motion_journal_survives_crash_and_keeps_original_order(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'state.json'
            journal=module.StartupJournal(path,{'order':{'id':'old','status':'done'}})
            request=journal.begin('arm2','BUILD_SLIDE')
            saved=json.loads(path.read_text())
            self.assertEqual(saved['order']['id'],'old')
            self.assertEqual(saved['full_reset']['task']['id'],request)
            self.assertTrue(module.unresolved(saved))
            journal.accepted()
            journal.result(False,uncertain=True,error='timeout')
            saved=json.loads(path.read_text())
            self.assertTrue(saved['full_reset']['task']['accepted'])
            self.assertTrue(module.unresolved(saved))
    def test_startup_last_result_marks_done_but_failure_does_not(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'state.json'
            journal=module.StartupJournal(path,{})
            journal.begin('M2','GO_TO_PARK');journal.result(False,error='rejected')
            self.assertEqual(json.loads(path.read_text())['full_reset']['status'],'failed')
            journal.begin('M2','GO_TO_PARK');journal.accepted();journal.result(True)
            saved=json.loads(path.read_text())
            self.assertEqual(saved['full_reset']['status'],'done')
            self.assertIsNone(saved['full_reset']['task'])
            self.assertFalse(module.unresolved(saved))
    def test_unresolved_order_only_starts_warehouse_listener_for_recovery(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'order.json';path.write_text(json.dumps({'order':{'status':'failed'}}))
            with patch.dict(module.os.environ,ROS_DOMAIN_ID='40',HOST_MOCK='0',HOST_STATE_FILE=str(path)),patch.object(module.subprocess,'run') as remote:
                module.main();remote.assert_called_once()
                self.assertEqual(remote.call_args.args[0][-1],'python3 - warehouse')
                self.assertEqual(json.loads(path.read_text()),{'order':{'status':'failed'}})
    def test_mock_domain_cannot_launch_real_preparation(self):
        with patch.dict(module.os.environ,ROS_DOMAIN_ID='149',HOST_MOCK='1'),patch.object(module.subprocess,'run') as remote:
            with self.assertRaises(RuntimeError):module.main()
            remote.assert_not_called()


if __name__=='__main__':unittest.main()
