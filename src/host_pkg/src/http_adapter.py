"""Authenticated local API bridge. Network I/O never blocks the ROS executor."""
import copy
import json
import queue
import threading
import time
from urllib.request import Request, build_opener, ProxyHandler
import uuid


class HttpAdapter:
    def __init__(self, token, url='http://127.0.0.1:8082'):
        if not token:
            raise ValueError('ROBOT3_BRIDGE_TOKEN이 필요합니다. 통합 실행기를 사용하세요.')
        self.token, self.url = token, url
        self.instance = uuid.uuid4().hex
        self.commands = queue.Queue()
        self.lock = threading.Lock()
        self.latest = None
        self.last_contact = 0.0
        self.session = None
        self.revision = 0
        self.stopping = threading.Event()
        self.thread = threading.Thread(target=self.run, name='host-http-adapter', daemon=True)
        self.opener = build_opener(ProxyHandler({}))

    def start(self):
        self.thread.start()

    def set_report(self, report):
        with self.lock:
            self.latest = copy.deepcopy(report)

    def connected(self):
        return time.monotonic() - self.last_contact < 2.5

    def request(self, path, data=None):
        request = Request(self.url + path, None if data is None else json.dumps(data).encode(),
                          {'Content-Type': 'application/json', 'X-Bridge-Token': self.token})
        with self.opener.open(request, timeout=0.7) as response:
            return json.load(response)

    def run(self):
        while not self.stopping.is_set():
            with self.lock:
                report = copy.deepcopy(self.latest)
            if report is not None:
                try:
                    self.revision += 1
                    report.update(revision=self.revision, controller_id=self.instance)
                    state = self.request('/api/live/report', report)
                    session = state['bridge_session']
                    if self.session and session != self.session:
                        self.commands.put({'action': '_session_changed'})
                    self.session = session
                    for command in self.request('/api/live/commands'):
                        if command.get('controller_id') == self.instance:
                            self.commands.put(command)
                    self.last_contact = time.monotonic()
                except (OSError, ValueError, KeyError):
                    pass  # monotonic watchdog pauses progression; reconnect never replays steps
            self.stopping.wait(0.2)

    def close(self):
        self.stopping.set()
        self.thread.join(timeout=2)
