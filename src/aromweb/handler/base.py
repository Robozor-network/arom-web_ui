#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.escape
import tornado.web

import glob

import rosparam

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def initialize(self):
        #self.config = self.settings['']
        #self.db = self.settings['']
        pass
        
    def get_current_user(self):
        pass


class NodeHandler(BaseHandler):
    def get(self, node):
        user_data = self.get_current_user()

        try:
            params = rosparam.get_param("/arom/node/"+node)
            self.render("../template/node.hbs", user_data=user_data, NavItems=[], NodeParams = params, FeatureParams = None)
        except Exception, e:
            self.render("../template/nonode.hbs", user_data=user_data, NavItems=[], NodeParams = None, FeatureParams = None)



class MainHandler(BaseHandler):
    def get(self):
        user_data = self.get_current_user()
        self.render("../template/home.hbs", user_data=user_data, NavItems=[])