import os
from pathlib import Path
import tempfile
import unittest

from cell_remote import stale_server_modules


class ServerFreshnessTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.app=Path(self.temp.name)
        for name in ('action_server.py','action_protocol.py','linear_client.py',
                     'network_ready.py','episode_cli.py','episode_recovery.py'):
            path=self.app/name
            path.write_text('# fixture\n')
            os.utime(path,(100,100))

    def test_new_child_code_does_not_require_listener_restart(self):
        for name in ('episode_cli.py','episode_recovery.py'):
            os.utime(self.app/name,(300,300))
        self.assertEqual(stale_server_modules(self.app,200),[])

    def test_changed_resident_modules_still_require_restart(self):
        for name in ('action_server.py','action_protocol.py','linear_client.py','network_ready.py'):
            with self.subTest(name=name):
                os.utime(self.app/name,(300,300))
                self.assertEqual(stale_server_modules(self.app,200),[name])
                os.utime(self.app/name,(100,100))

    def test_restart_after_changes_clears_requirement(self):
        os.utime(self.app/'action_server.py',(300,300))
        self.assertEqual(stale_server_modules(self.app,400),[])

    def test_missing_resident_source_is_not_silently_accepted(self):
        (self.app/'action_protocol.py').unlink()
        with self.assertRaises(FileNotFoundError):stale_server_modules(self.app,200)


if __name__=='__main__':unittest.main()
