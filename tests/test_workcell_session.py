import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/host_pkg/src'))
from workcell_session import Lease

class LeaseTests(unittest.TestCase):
    def setUp(self):
        self.now=0;self.lease=Lease('a'*32,lambda:self.now)
    def receive(self,**data):return self.lease.receive(json.dumps(data))
    def challenge(self,nonce='n',epoch='e'):
        return self.receive(kind='challenge',epoch=epoch,nonce=nonce)
    def ack(self,nonce='n',epoch='e',client_id='a'*32):
        self.receive(kind='ack',epoch=epoch,nonce=nonce,client_id=client_id)
    def test_requires_matching_roundtrip(self):
        self.assertFalse(self.lease.ready())
        with self.assertRaises(RuntimeError):self.lease.encode('CLEAR_ERROR','b'*32)
        self.assertEqual(self.lease.encode('EMER_STOP','b'*32),'EMER_STOP')
        self.assertEqual(json.loads(self.challenge())['client_id'],'a'*32)
        self.ack(client_id='c'*32);self.assertFalse(self.lease.ready())
        self.ack();self.assertTrue(self.lease.ready())
        first=json.loads(self.lease.encode('CLEAR_ERROR','b'*32));second=json.loads(self.lease.encode('CLEAR_ERROR','b'*32))
        self.assertEqual(first['version'],2);self.assertEqual(first['request_id'],second['request_id'])
        self.assertNotEqual(first['attempt_id'],second['attempt_id'])
    def test_stale_replay_does_not_extend_lease(self):
        self.challenge();self.ack();self.now=1
        self.challenge();self.ack();self.now=1.6
        self.assertFalse(self.lease.ready());self.ack();self.assertFalse(self.lease.ready())
    def test_server_restart_invalidates_ack(self):
        self.challenge();self.ack();self.challenge(epoch='new');self.ack()
        self.assertFalse(self.lease.ready());self.ack(epoch='new');self.assertTrue(self.lease.ready())
    def test_delayed_ack_cannot_replace_newer_lease(self):
        self.challenge('old');self.now=.5;self.challenge('new');self.ack('new');self.ack('old')
        self.assertEqual(self.lease.ack[1],'new')
    def test_invalid_input_ignored(self):
        for value in ['bad','[]','null','{"kind":"challenge"}']:
            self.assertIsNone(self.lease.receive(value));self.assertFalse(self.lease.ready())

if __name__=='__main__':unittest.main()
