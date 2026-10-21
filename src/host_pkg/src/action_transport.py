"""Nonblocking clients for the deployed Burger/Arm Action contracts."""
import uuid
from rclpy.action import ActionClient
from host_pkg.action import Arm, Burger
from unique_identifier_msgs.msg import UUID
from control import DEVICES


class ActionTransport:
    def __init__(self, node, events, speed=30.0):
        self.events, self.speed = events, speed
        self.clients = {device: ActionClient(node, Burger if device in ('M1', 'M2') else Arm,
                                             f'/{device}/data') for device in DEVICES}

    def ready(self):
        return {device: client.server_is_ready() for device, client in self.clients.items()}

    def send(self, task):
        self.submit(task['device'], task['command'], task['id'])

    def prepare_parked(self, task):
        from parked_preparation import start
        start(task, self.events)

    def stop(self, device):
        request_id = uuid.uuid4().hex
        self.submit(device, 'EMER_STOP', request_id, control=True)
        return request_id

    def submit(self, device, command, request_id, control=False):
        client = self.clients[device]
        kind = 'stop' if control else 'done'
        def finish(data):
            self.events.put((request_id, kind, dict(data, device=device)))
        def result(future):
            try:
                wrapped = future.result()
                finish({'status': wrapped.status, 'success': wrapped.result.success,
                        'message': wrapped.result.message})
            except Exception as exc:
                finish({'status': 0, 'success': False, 'message': str(exc), 'uncertain': True})
        def accepted(future):
            try:
                handle = future.result()
                if not handle.accepted:
                    finish({'status': 0, 'success': False, 'message': 'Goal 거절', 'rejected': True})
                    return
                if not control:
                    self.events.put((request_id, 'accepted', {}))
                handle.get_result_async().add_done_callback(result)
            except Exception as exc:
                finish({'status': 0, 'success': False, 'message': str(exc), 'uncertain': True})
        def feedback(message):
            if not control:
                self.events.put((request_id, 'feedback', {'message': message.feedback.message}))
        try:
            if not client.server_is_ready():
                finish({'status': 0, 'success': False, 'message': 'Action 서버 미연결', 'not_sent': True})
                return
            goal = Burger.Goal() if device in ('M1', 'M2') else Arm.Goal()
            goal.command = command
            if device in ('M1', 'M2'):
                goal.cmd_val = self.speed if command.startswith('GO_TO_') and not control else 0.0
            future = client.send_goal_async(goal, feedback_callback=feedback,
                                            goal_uuid=UUID(uuid=list(uuid.UUID(hex=request_id).bytes)))
            future.add_done_callback(accepted)
        except Exception as exc:
            finish({'status': 0, 'success': False, 'message': str(exc), 'uncertain': True})
