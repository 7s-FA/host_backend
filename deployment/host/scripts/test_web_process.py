#!/usr/bin/env python3
import os
from pathlib import Path
import subprocess
from test_full_process import stack, ROOT

node = Path('/home/operator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node')
env = dict(os.environ, NODE_PATH=str(node / 'node_modules'), CHROME_PATH='/usr/bin/google-chrome')
with stack('browser', delay='1.2', timeout='30'):
    subprocess.run([str(node / 'bin/node'), str(ROOT / 'host_web/tests/control-browser.cjs')], env=env, check=True)
    subprocess.run([str(node / 'bin/node'), str(ROOT / 'scripts/test_control_browser.cjs')], env=env, check=True)
