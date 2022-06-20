'''In this file you need to implement remote procedure call (RPC) server

* There are different RPC libraries for python, such as xmlrpclib, json-rpc. You are free to choose.
* The following functions have to be implemented and exported:
 * get_angle
 * set_angle
 * get_posture
 * execute_keyframes
 * get_transform
 * set_transform
* You can test RPC server with ipython before implementing agent_client.py
'''

# add PYTHONPATH

import os
import sys
import threading

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'kinematics'))

import inverse_kinematics

# Path Restriction
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class ServerAgent(InverseKinematicsAgent):
    '''ServerAgent provides RPC service
    '''
    # YOUR CODE HERE
    
    def get_angle(self, joint_name):
        '''get sensor value of given joint'''
        # YOUR CODE HERE
        print("Get-angle is being executed")
        return self.target_joints.get(joint_name)
    
    def set_angle(self, joint_name, angle):
        '''set target angle of joint for PID controller
        '''
        # YOUR CODE HERE
        print("Set-angle is being executed")
        self.target_joints[joint_name] = angle


def get_posture(self):
        '''return current posture of robot'''
        # YOUR CODE HERE
        print("Get-posture is being executed")
        return self.recognize_posture(self.perception)


def execute_keyframes(self, keyframes):
        '''excute keyframes, note this function is blocking call,
        e.g. return until keyframes are executed
        '''
        # YOUR CODE HERE
        print("Execute_keyframes is being executed")
        self.keyframes = keyframes


    def get_transform(self, name):
        '''get transform with given name
        '''
        # YOUR CODE HERE
        return self.transforms[name]

    def set_transform(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        # YOUR CODE HERE
        self.set_transforms(effector_name, transform)



if __name__ == '__main__':
    print("------------ Starting Agent ------------ ")
    agent = ServerAgent()

    server = SimpleXMLRPCServer( ("localhost", 8000), requestHandler=RequestHandler)
    server.register_function(ServerAgent.get_angle, 'get_angle')
    server.register_function(ServerAgent.set_angle, 'set_angle')
    server.register_function(ServerAgent.get_posture, 'get_posture')
    server.register_function(ServerAgent.execute_keyframes, 'execute_keyframes')
    server.register_function(ServerAgent.get_transform, 'get_transform')
    server.register_function(ServerAgent.set_transform, 'set_transform')
    server.register_introspection_functions()
    server.register_multicall_functions()
    server.register_instance(agent)


    thread = threading.Thread(target=server.serve_forever)
    thread.start()

    print("------------ Server started on localhost:8000 ------------")
    agent.run()

