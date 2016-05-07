
#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
import tornado.ioloop
import tornado.web
from tornado import web
from tornado import ioloop
from tornado import websocket
from tornado import auth
from tornado import escape
from tornado import httpserver
from tornado import options
from tornado import web
import json
import ephem

import std_msgs
from std_msgs.msg import String
from std_msgs.msg import Float32
from arom.srv import *
from arom.msg import *
import rospy

from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import Angle
from astropy.coordinates import EarthLocation
from astropy.coordinates import AltAz
from astropy.time import Time
import rosapi
import MySQLdb as mdb

#print rosapi.get_nodes()

observatory = EarthLocation(lat=49*u.deg, lon=14*u.deg, height=300*u.m)

leftmenu = [["observatory", "observatory"],["Vec 1", "#"], ["Vec 2", "#"], ["Vec 3", "#"], ["Mount", "mount"]]
leftmenu = [["observatory", "observatory"], ["Mount", "mount"]]

rospy.logerr("wait_for_service /arom/NodeInfo")
print "wait_for_service /arom/NodeInfo"
rospy.wait_for_service('/arom/NodeInfo')
#brain_nodeinfo = rospy.ServiceProxy('/arom/NodeInfo', arom.srv.NodeInfo)

def get_devices():
    try:    
        print "ZIskavam tady data NodeInfo"
        brain_nodeinfo = rospy.ServiceProxy('/arom/NodeInfo', arom.srv.NodeInfo)
        resp1 = brain_nodeinfo(type = 'GetAllNodes')
        print resp1
        print "--------------------"
        return resp1
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


def _sql(query, read=False):
        print "#>", query
        connection = mdb.connect(host="localhost", user="root", passwd="root", db="AROM", use_unicode=True, charset="utf8")
        cursorobj = connection.cursor()
        result = None
        try:
                cursorobj.execute(query)
                result = cursorobj.fetchall()
                if not read:
                    connection.commit()
        except Exception, e:
                print "Err", e
        connection.close()
        return result


class Overview(web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, addres=None):
        print "web", addres
        self.render("www/layout/dash/publicOverview.html", title = "AROM", leftmenu = leftmenu, actual = '#', _sql=_sql)

class Mount(web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, addres=None):
        print "web", addres
        self.render("www/layout/dash/mount.html", title = "AROM control center | mount", leftmenu = leftmenu, actual = 'mount', _sql=_sql)

class Observatory(web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, addres=None):
        print "web", addres
        self.render("www/layout/dash/observatory.html", title = "AROM control center | observatory", leftmenu = leftmenu, actual = 'observatory', _sql=_sql)

class Obs_weather_datatable(web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, addres=None):
        arg_data = self.get_argument('data', False)
        arg_type = self.get_argument('type', False)
        arg_sens = self.get_argument('sens', 0)
        print arg_type, arg_data, "---------"
        if arg_data == 'weather' and arg_type == 'json':
            data = _sql('SELECT date, avg(value), sensors_id from weather GROUP BY date div (60*10), sensors_id  ORDER BY date;')
            self.write('[\n\r['+str(float(data[0][0])*1000)+','+str(round(float(data[0][1]),3))+','+str(round(float(data[0][2]),3))+']')
            for row in data:
                self.write(',['+str(float(row[0])*1000)+','+str(round(float(row[1]),3))+','+str(round(float(row[2]),3))+']\n\r')
                #sout.append([float(row[0]), float(row[1])])
            self.finish('\n\r]')

        elif arg_data == 'AROMconfig' and arg_type == 'json':
            pass
        else:
            data = _sql('SELECT weather.id, weather.date, weather.sensors_id, weather.value, sensors.sensor_name, sensors.sensor_quantity_mark FROM weather JOIN sensors ON weather.sensors_id = sensors.sensors_id WHERE (date > %f) GROUP BY sensors_id ORDER BY weather.sensors_id;' %(Time.now().unix-60))
            print data
            string = '<table class="table">'
            for row in data:
                string += '<tr><td>'+datetime.datetime.fromtimestamp(float(row[1])).strftime('%Y-%m-%d %H:%M:%S')+'</td><td>'+str(row[4])+'</td><td>'+str(row[2])+'</td><td>'+str(row[3])+" "+row[5]+'</td></tr>'
            string += '</table>'
            self.finish(string)

class DriverPage(web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, addres=None):
        print "web", addres
        #self.render("www/layout/dash/observatory.html", title = "AROM control center | observatory", leftmenu = leftmenu, actual = 'observatory', _sql=_sql)
        self.finish("loading...")

class Obs_config_diagram(web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, addres=None):
        self.render("www/layout/dash/tools/ConfigDiagram.html", _sql=_sql)
        


class processing(web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, arg = None):
        rospy.logerr("processing")
        print "processing", arg
        coord = self.get_argument("coord", False)
        if coord:
            param = eval(coord)
            print "param", param
            if param['typ'] == 'AltAz2RaDec':
                out = SkyCoord(alt=param['alt'], az=param['az'], unit='deg', obstime = Time.now(), frame = 'altaz', location = observatory)
                sout = {
                    "ra": out.icrs.ra.degree,
                    "dec": out.icrs.dec.degree,
                    #"alt": param['alt'],
                    #"az": param['az'],
                    }
                print sout
                self.finish(escape.json_encode(sout))

                
            elif param['typ'] == 'RaDec2AltAz':
                # = loc.transform_to(AltAz(obstime = Time.now(), location=self.observatory))
                #F_az = (np.abs(self.horizont[:,0] - altaz.az.degree)).argmin()
                #local_horizont = self.horizont[F_az]
                pass
        else:
            rospy.logerr("Chyba v processing")

class bootstrap(web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, addres=None):
        self.render("www/layout/dash/bootstrap.html", _sql=_sql, devices = get_devices())
        
class bootstrap_setting(web.RequestHandler):
    def get(self):
        self.render("www/layout/dash/bootstrap_setting.html", _sql=_sql, devices = get_devices())
        
        


app = web.Application([
        (r'/', Overview),
        (r'/bootstrap/setting', bootstrap_setting),
        (r'/bootstrap/(.*)', bootstrap_setting),
        (r'/bootstrap', bootstrap),
        (r'/mount', Mount),
        (r'/observatory/weather/(.*)', Obs_weather_datatable),
        (r'/observatory/cfg/(.*)', Obs_config_diagram),
        (r'/observatory', Observatory),
        (r'/obs', Observatory),
        (r'/processing', processing),
        (r'/processing(.*)', processing),
        (r'/driver/(.*)', DriverPage),
       # (r'/multibolid(.*)', MultiBolid),
       # (r'/multibolid', MultiBolid),
       # (r'/realtime(.*)', RTbolidozor),
       # (r'/realtime', RTbolidozor),
       
        (r'/(favicon.ico)', web.StaticFileHandler, {'path': '.www/media/favicon.ico'}),
        (r'/fonts/(.*)', tornado.web.StaticFileHandler,{"path": './www/fonts/' }),
        (r"/lib/(.*)", tornado.web.StaticFileHandler,{"path": './www/lib/' }),
        (r"/(.*\.png)", tornado.web.StaticFileHandler,{"path": './www/media/' }),
        (r"/(.*\.jpg)", tornado.web.StaticFileHandler,{"path": './www/media/' }),
        (r"/(.*\.ogg)", tornado.web.StaticFileHandler,{"path": './www/media/' }),
        (r"/(.*\.wav)", tornado.web.StaticFileHandler,{"path": './www/media/' }),
        (r"/(.*\.woff2)", tornado.web.StaticFileHandler,{"path": './www/fonts/' }),
        (r"/(.*\.css)", tornado.web.StaticFileHandler,{"path": './www/css/' }),
        (r"/(.*\.wav)", tornado.web.StaticFileHandler,{"path": './www/wav/' }),
        (r"/(.*\.json)", tornado.web.StaticFileHandler,{"path": './www/json/' }),
        (r"/(.*\.js)", tornado.web.StaticFileHandler,{"path": './www/js/' }),
       #(r"/static/(.*)", web.StaticFileHandler, {"path": "/var/www"}),
        (r"/(.*)", Overview),
    ],
    cookie_secret="ROT13IrehaxnWrArwyrcfvQvixnAnFirgr",
    debug=True,
    autoreload=True)

def main():
    app.listen(5252)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()