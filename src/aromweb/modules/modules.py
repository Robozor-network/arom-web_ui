#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado
import rosnode

class WeatherInfo(tornado.web.UIModule):

    def render(self):
        return self.render_string("modules/WeatherInfo.hbs")
        #return "self.render_string()"


class NavBar(tornado.web.UIModule):
    def render(self):
        #rosnode.rosnode_listnodes(list_all=True)
        return self.render_string("nav.hbs", navItems = rosnode.get_node_names())


class NodeFeature(tornado.web.UIModule):
    def render(self, node, *args, **kwds):
        #return globals()[node](self, *args, **kwds).value()
        return self.render_string("modules/features/%s.hbs"%(node), FeatureParams = args[0])

########################################################################################
##
##                         Node features
##

'''
class display_control():
    def __init__(self, parent, *args, **kwds):
        self.parent = parent
        self.args = args

    def value(self):
        return self.parent.render_string("modules/features/display_control.hbs", FeatureParams = self.args[0])


class display_show():
    def __init__(self, parent, *args, **kwds):
        self.parent = parent
        self.args = args

    def value(self):
        return self.parent.render_string("modules/features/display_show.hbs", FeatureParams = self.args[0])



class gpio_set_port():
    def __init__(self, parent, *args, **kwds):
        self.parent = parent
        self.args = args

    def value(self):
        return self.parent.render_string("modules/features/gpio_set_port.hbs", FeatureParams = self.args[0])

class gpio_all_off():
    def __init__(self, parent, *args, **kwds):
        self.parent = parent
        self.args = args

    def value(self):
        return self.parent.render_string("modules/features/gpio_all_off.hbs", FeatureParams = self.args[0])


class mount_slew():
    def __init__(self, parent, *args, **kwds):
        self.parent = parent
        self.args = args

    def value(self):
        return self.parent.render_string("modules/features/mount_slew.hbs", FeatureParams = self.args[0])

class mount_skymap():
    def __init__(self, parent, *args, **kwds):
        self.parent = parent
        self.args = args

    def value(self):
        return self.parent.render_string("modules/features/mount_skymap.hbs", FeatureParams = self.args[0])
'''