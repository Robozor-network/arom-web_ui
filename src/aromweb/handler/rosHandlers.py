#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.escape
import tornado.web

import glob

import rosparam
import rospy
from std_msgs.msg import String

class publish(tornado.web.RequestHandler):    # /rosapi/publist/(.*)

    def get(self, type):
        if type == 'string':
            topic = self.get_argument('topic', '/rosout')
            data = self.get_argument('data', 'None')
            pub = rospy.Publisher('topic', String, queue_size=10)
            rospy.init_node('web_publisher')
            print(pub, topic, data)
            pub.publish(String(data))
            self.write("ack")
