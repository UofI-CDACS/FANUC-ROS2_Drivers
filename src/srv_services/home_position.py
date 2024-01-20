#!/usr/bin/env python3
import sys
import os
import rclpy

sys.path.append("src/dependencies/")
import FANUCethernetipDriver

from robot_controller import robot
from fanuc_interfaces.srv import Home
from rclpy.node import Node

FANUCethernetipDriver.DEBUG = False

sys.path.append('./pycomm3/pycomm3')

# Robot IP is passed as command line argument 1
robot_ip = sys.argv[1]

# Quick and dirty
if robot_ip == '172.29.208.124':
	name = "beaker"
elif robot_ip == '172.29.208.123':
     name = "bunsen"
else:
	name = "rogue"
     
    
class go_home(Node):
    def __init__(self):
        super().__init__('home_srv')
        self.bot = robot(robot_ip)
        self.srv = self.create_service(Home, f'{name}/go_home', self.service_callback)

    def service_callback(self, request, response):
        self.bot.set_joints_to_home_position()
        self.bot.start_robot(blocking=False)
        try:
            while self.bot.is_moving(): # Verify that it actually completed
                pass
        except:
            response.success = False  # If here, there was some kind of error      
        
        response.success = True   # Otherwise, evrything went well
        if FANUCethernetipDriver.DEBUG:
            self.get_logger().info('Incoming request result: ',response.success)
	
        return response


def main(args=None):
    rclpy.init(args=args)

    publisher = go_home()

    rclpy.spin(publisher)

    publisher.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
    
