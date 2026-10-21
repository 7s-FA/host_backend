"""ROS startup response recovery smoke test; domain 149 / LOCALHOST only."""
import sys,time,threading,uuid,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer,ActionClient
from rclpy.executors import MultiThreadedExecutor
from unique_identifier_msgs.msg import UUID
from host_pkg.action import Arm,Burger
from startup_action import release_once
assert os.environ['ROS_DOMAIN_ID']=='149'
assert os.environ['ROS_AUTOMATIC_DISCOVERY_RANGE']=='LOCALHOST'
rclpy.init();node=Node('startup_result_test');executor=MultiThreadedExecutor(num_threads=4);executor.add_node(node)
counts={};servers=[];clients=[];queries=[]
def wait(f,seconds,label):
    deadline=time.monotonic()+seconds
    while not f.done() and time.monotonic()<deadline:time.sleep(.01)
    if not f.done():raise TimeoutError(label)
    return f.result()
for action,name,command in [(Burger,'/fake/M2','RESTART'),(Arm,'/fake/arm1','CLEAR_ERROR')]:
    counts[name]=0
    def execute(handle,action=action,name=name):
        counts[name]+=1;handle.succeed();r=action.Result();r.success=True;r.message='IDLE';return r
    servers.append(ActionServer(node,action,name,execute_callback=execute))
    clients.append(ActionClient(node,action,name))
    queries.append(node.create_client(action.Impl.GetResultService,name+'/_action/get_result'))
t=threading.Thread(target=executor.spin);t.start()
try:
    for i,(action,name,command) in enumerate([(Burger,'/fake/M2','RESTART'),(Arm,'/fake/arm1','CLEAR_ERROR')]):
        assert clients[i].wait_for_server(timeout_sec=5)
        def query(goal_id,seconds):
            req=action.Impl.GetResultService.Request();req.goal_id=goal_id
            return wait(queries[i].call_async(req),seconds,'result query')
        unknown=query(UUID(uuid=list(uuid.uuid4().bytes)),5);assert unknown.status==0
        for drop_acceptance in (False,True):
            def lossy_wait(f,seconds,label):
                result=wait(f,seconds,label)
                if drop_acceptance and label.endswith('접수'):raise TimeoutError('simulated lost acceptance')
                return result
            goal=action.Goal();goal.command=command
            release_once(clients[i],goal,UUID(uuid=list(uuid.uuid4().bytes)),lossy_wait,query,5,name)
        assert counts[name]==2,counts
        print('PASS actual ROS types, unknown-goal preflight, normal result, lost acceptance, no duplicate:',name)
finally:
    executor.shutdown();t.join()
    for client in clients:client.destroy()
    for server in servers:server.destroy()
    node.destroy_node();rclpy.shutdown()
