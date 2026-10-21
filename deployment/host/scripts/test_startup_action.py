import unittest
from types import SimpleNamespace as NS
from unittest.mock import Mock

from startup_action import release_once


def reply(status=4, success=True, message='IDLE'):
    return NS(status=status,result=NS(success=success,message=message))


class StartupActionTests(unittest.TestCase):
    def setUp(self):
        self.client=Mock()
        self.goal=NS(command='RESTART')
        self.goal_id=object()
        self.handle=Mock(accepted=True)

    def call(self,wait,query):
        return release_once(self.client,self.goal,self.goal_id,wait,query,15,'M2 RESTART',Mock())

    def assert_one_goal(self):
        self.client.send_goal_async.assert_called_once_with(self.goal,goal_uuid=self.goal_id)

    def test_normal_result_needs_no_fallback(self):
        result=reply();query=Mock()
        self.assertIs(self.call(Mock(side_effect=[self.handle,result]),query),result)
        query.assert_not_called();self.assert_one_goal()

    def test_lost_acceptance_recovers_only_same_goal(self):
        result=reply();query=Mock(return_value=result)
        self.assertIs(self.call(Mock(side_effect=TimeoutError()),query),result)
        query.assert_called_once_with(self.goal_id,15);self.assert_one_goal()

    def test_lost_result_recovers_without_resending(self):
        query=Mock(return_value=reply())
        self.call(Mock(side_effect=[self.handle,TimeoutError()]),query)
        query.assert_called_once_with(self.goal_id,15);self.assert_one_goal()

    def test_unknown_aborted_cancelled_or_invalid_success_never_passes(self):
        for result in (reply(0),reply(6),reply(5),reply(success=False),reply(message='ERROR')):
            with self.subTest(result=result),self.assertRaises(RuntimeError):
                self.call(Mock(side_effect=TimeoutError()),Mock(return_value=result))

    def test_query_timeout_remains_failure(self):
        with self.assertRaises(TimeoutError):
            self.call(Mock(side_effect=TimeoutError()),Mock(side_effect=TimeoutError()))
        self.assert_one_goal()

    def test_rejected_goal_is_not_queried_or_retried(self):
        query=Mock()
        with self.assertRaises(RuntimeError):
            self.call(Mock(return_value=NS(accepted=False)),query)
        query.assert_not_called();self.assert_one_goal()

    def test_home_and_route_commands_cannot_use_release_recovery(self):
        for command in ('HOME_A','PREPARE_HOME','GO_TO_MAT'):
            self.goal.command=command
            with self.assertRaises(ValueError):self.call(Mock(),Mock())
        self.client.send_goal_async.assert_not_called()


if __name__=='__main__':unittest.main()
