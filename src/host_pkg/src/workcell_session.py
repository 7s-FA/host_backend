"""V2 workcell lease: echo fresh challenges; execute only after matching ACK."""
import json
import time
import uuid

STATUS_TOPIC = '/workcell/supervision/status'
HEARTBEAT_TOPIC = '/workcell/supervision/heartbeat'


class Lease:
    def __init__(self, client_id=None, clock=time.monotonic):
        self.client_id = client_id or uuid.uuid4().hex
        self.clock = clock
        self.epoch = None
        self.pending = {}
        self.ack = None

    def receive(self, text):
        try: value = json.loads(text)
        except (ValueError, TypeError): return None
        if not isinstance(value, dict): return None
        epoch, nonce = value.get('epoch'), value.get('nonce')
        if not all(isinstance(x,str) and 0<len(x)<=128 for x in (epoch,nonce)): return None
        now = self.clock()
        self.pending = {k:v for k,v in self.pending.items() if now-v<1.5}
        if value.get('kind') == 'challenge':
            if self.epoch != epoch:
                self.epoch, self.ack, self.pending = epoch, None, {}
            # Duplicate/buffered delivery must never refresh the original age.
            if nonce in self.pending: return None
            self.pending[nonce] = now
            return json.dumps(dict(client_id=self.client_id, epoch=epoch, nonce=nonce))
        if (value.get('kind') == 'ack' and value.get('client_id') == self.client_id
                and epoch == self.epoch and nonce in self.pending):
            issued = self.pending[nonce]
            if now-issued<1.5 and (self.ack is None or issued>self.ack[2]):
                self.ack = (epoch, nonce, issued)
        return None

    def ready(self):
        return self.ack is not None and 0<=self.clock()-self.ack[2]<1.5

    def encode(self, command, request_id):
        if not self.ready():
            if command == 'EMER_STOP': return command
            raise RuntimeError('제작공정 V2 양방향 연결 확인 대기')
        return json.dumps(dict(version=2, client_id=self.client_id, request_id=request_id,
                               attempt_id=uuid.uuid4().hex, command=command,
                               epoch=self.ack[0], nonce=self.ack[1]))


class WorkcellSession:
    def __init__(self, node):
        from std_msgs.msg import String
        from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
        self.lease = Lease()
        self.String = String
        qos = QoSProfile(depth=1, reliability=ReliabilityPolicy.BEST_EFFORT,
                         durability=DurabilityPolicy.VOLATILE)
        self.publisher = node.create_publisher(String, HEARTBEAT_TOPIC, qos)
        self.subscription = node.create_subscription(String, STATUS_TOPIC, self.receive, qos)

    def receive(self, message):
        reply = self.lease.receive(message.data)
        if reply: self.publisher.publish(self.String(data=reply))
