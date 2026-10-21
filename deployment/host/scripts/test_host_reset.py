"""Reset CLI tests use only mocked HTTP replies; never contact equipment."""
import contextlib
import io
import unittest
from unittest.mock import patch

import host_reset


class ResetCliTest(unittest.TestCase):
    def setUp(self):
        self.state = {'bridge_connected': True, 'can_reset': True,
                      'order': {'id': 'failed-order', 'status': 'failed'}}

    def run_cli(self, replies, answer='초기화'):
        with patch.object(host_reset.sys, 'argv', ['hostreset']), \
             patch.object(host_reset, 'request', side_effect=replies) as request, \
             patch('builtins.input', return_value=answer), \
             patch.object(host_reset.time, 'sleep'), contextlib.redirect_stdout(io.StringIO()):
            result = host_reset.main()
            return result, request.call_args_list

    def test_unconfirmed_does_not_post(self):
        result, calls = self.run_cli([self.state], '아니오')
        self.assertEqual(result, 0)
        self.assertEqual(len(calls), 1)

    def test_offline_or_running_or_blocked_never_posts(self):
        for state in ({**self.state, 'bridge_connected': False},
                      {**self.state, 'can_reset': False},
                      {**self.state, 'order': {'status': 'running'}}):
            result, calls = self.run_cli([state])
            self.assertEqual(result, 1)
            self.assertEqual(len(calls), 1)

    def test_reset_is_bound_to_order_and_waits_for_final_result(self):
        result, calls = self.run_cli([self.state, {},
                                     {**self.state, 'reset_pending': True},
                                     {'bridge_connected': True, 'order': None}])
        self.assertEqual(result, 0)
        self.assertEqual(calls[1].args,
                         ('reset', {'order_id': 'failed-order', 'operator_confirmed': True}))
        self.assertEqual([c.args[0] for c in calls], ['state', 'reset', 'state', 'state'])

    def test_rejected_reset_is_not_reported_as_success(self):
        result, calls = self.run_cli([self.state, {}, {**self.state, 'latest_event': '정지 실패'}])
        self.assertEqual(result, 1)
        self.assertEqual(len(calls), 3)


if __name__ == '__main__':
    unittest.main()
