#!/usr/bin/env python3
"""Verify SSH startup guards with fake SSH/systemd; no network or robot actions."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class StartupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        self.events = self.path / 'events.jsonl'
        self.state = self.path / 'state'
        self.state.write_text('inactive')
        self.env = dict(os.environ, PATH=str(self.path) + ':' + os.environ['PATH'],
                        AMR_TEST_EVENTS=str(self.events), AMR_TEST_STATE=str(self.state))
        self.program('systemctl', '''
import json,os,sys
from pathlib import Path
args=sys.argv[1:]
with open(os.environ['AMR_TEST_EVENTS'],'a') as f: f.write(json.dumps(args)+'\\n')
state=Path(os.environ['AMR_TEST_STATE'])
if 'LoadState' in args: print(os.environ.get('AMR_TEST_LOAD','loaded'))
elif 'start' in args: state.write_text('active')
elif '--value' in args: print(state.read_text())
else: print('ActiveState='+state.read_text()+'\\nSubState=running\\nMainPID=123')
''')
        self.program('ssh', '''
import json,os,sys
with open(os.environ['AMR_TEST_EVENTS'],'a') as f: f.write(json.dumps(sys.argv[1:])+'\\n')
sys.stdin.read()
sys.exit(int(os.environ.get('AMR_TEST_SSH_EXIT','0')))
''')

    def program(self, name, source):
        script = self.path / name
        script.write_text('#!/usr/bin/python3\n' + source)
        script.chmod(0o755)

    def run_script(self, name, *args):
        return subprocess.run(['bash', str(ROOT / name), *args], env=self.env,
                              capture_output=True, text=True, timeout=5)

    def calls(self):
        return [json.loads(line) for line in self.events.read_text().splitlines()] if self.events.exists() else []

    def test_active_server_is_never_restarted(self):
        self.state.write_text('active')
        result = self.run_script('scripts/amr_remote.bash', 'M1', 'start', 'false')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(any('start' in a or 'restart' in a or 'stop' in a for a in self.calls()))

    def test_inactive_server_is_started_once(self):
        result = self.run_script('scripts/amr_remote.bash', 'M2', 'start', 'false')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([a for a in self.calls() if 'start' in a],
                         [['--user', 'start', 'm2-action.service']])

    def test_failed_server_is_not_blindly_restarted(self):
        self.state.write_text('failed')
        result = self.run_script('scripts/amr_remote.bash', 'M1', 'start', 'false')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(any('start' in a for a in self.calls()))

    def test_status_does_not_start_inactive_service(self):
        result = self.run_script('scripts/amr_remote.bash', 'M2', 'status', 'false')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.state.read_text(), 'inactive')

    def test_ssh_failure_stops_before_second_robot(self):
        self.env['AMR_TEST_SSH_EXIT'] = '255'
        result = self.run_script('start_amr.sh')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(len(self.calls()), 1)
        self.assertIn('bash -s -- M1 start false', self.calls()[0])

    def test_parking_requires_explicit_preparation(self):
        result = self.run_script('start_amr.sh', '--parked')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls(), [])

    def test_explicit_preparation_targets_only_selected_robot(self):
        result = self.run_script('start_amr.sh', '--ready', '--parked', '--robot', 'M2')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(self.calls()), 1)
        self.assertIn('bash -s -- M2 ready true', self.calls()[0])


if __name__ == '__main__':
    unittest.main()
