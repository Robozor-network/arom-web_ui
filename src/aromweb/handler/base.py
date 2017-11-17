#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.escape
import tornado.web

import glob
import json
import io
import os, sys
import subprocess


import rosparam
import md5

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):

        user_file = '/home/odroid/robozor/users.json'

        #if not os.path.exists(user_file):
        #    print "Missing user.json (%s)" %(user_file)
        #    sys.exit()

        user_json = self.get_secure_cookie("user")
        with open(user_file) as data_file:    
            users = json.load(data_file)

        if user_json:
            return users[eval(user_json)]
        else:
            return None

    def initialize(self):
        #self.config = self.settings['']
        #self.db = self.settings['']
        pass
        
    def get_login_url(self):
        return u"/login"

class NodeStart(BaseHandler):
    def get(self, node):
        print "START", "test"
        print node
        if self.current_user:
            cmd = ['rosrun', 'arom', node, '&']
            r = subprocess.Popen(cmd)
            return self.write(" - ".join(cmd))
        else:
            return self.write("UserErr")

def PowerOff(BaseHandler):
    def get(self, name=None):
        if self.current_user:
            cmd = ['poweroff']
            r = subprocess.Popen(cmd)
            return self.write(" - ".join(cmd))
        else:
            return self.write("UserErr, zkuste se prihlasit")
        

class NodeKill(BaseHandler):
    def get(self, node):
        print "KILL"
        print node
        if self.current_user:
            cmd = ['rosnode', 'kill', '/'+node]
            r = subprocess.call(cmd)
            return self.write(repr(cmd))
        else:
            return self.write("UserErr")

class GetImage(BaseHandler):
    def get(self, node):
        print "GetImage"
        image_loc = self.get_argument("image", None)
        if image_loc:
            print image_loc
            img  = open(image_loc, "r")
            self.set_header ('Content-Type', 'image/jpg')
            #self.set_header ('Content-Disposition', 'attachment; filename='+filename+'')
            #self.write (image_loc)
            self.write (img.read())


        else:
            return self.write("No img")


class LoginHandler(BaseHandler):

    #def get(self):
    #    self.render("login.html", next=self.get_argument("next","/"))

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")

        with open('/home/odroid/robozor/users.json') as data_file:    
            users = json.load(data_file)

        print username
        print users

        if username in users:
            print "tento uzivatel existuje"
            print users[username]
            if users[username]['pass'] == md5.new(password).hexdigest():
                self.set_current_user(username)
                self.redirect(self.get_argument("next", u"/"))
            else:
                self.clear_cookie("user")
                self.redirect("/")
        else:
            self.clear_cookie("user")
            self.redirect("/")
            #error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect.")
            #self.redirect(u"/login" + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")

class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        self.redirect(u"/")

class NodeHandler(BaseHandler):
    def get(self, node):
        print self.current_user
        user_data = self.get_current_user()

        if self.current_user:
            try:
                params = rosparam.get_param("/arom/node/"+node)
                self.render("../template/node.hbs", user_data=user_data, NavItems=[], NodeParams = params, FeatureParams = None)
            except Exception, e:
                self.render("../template/nonode.hbs", user_data=user_data, NavItems=[], NodeParams = None, FeatureParams = None)
        else:
                self.render("../template/loggedout.hbs")



class MainHandler(BaseHandler):
    def get(self):
        user_data = self.get_current_user()
        self.render("../template/home.hbs", user_data=user_data, NavItems=[])


class WebApi(BaseHandler):
    def get(self, node):
        self.write("Hi")

class WebUpload(BaseHandler):
    def put(self, node):
        data = json.loads(self.request.body)
        print json.dumps(data, indent=4, sort_keys=False)
        print "test", '/'+node

        with io.open('/'+node, 'w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(data, indent=4, sort_keys=False, ensure_ascii=False)))


        
        