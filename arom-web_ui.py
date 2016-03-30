
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
        data = _sql('SELECT id, date, sensors_id, value FROM weather WHERE (date > %f)  GROUP BY sensors_id ORDER BY date DESC;' %(Time.now().unix-60))
        print data
        string = '<table class="table">'
        for row in data:
            string += '<tr><td>'+datetime.datetime.fromtimestamp(float(row[1])).strftime('%Y-%m-%d %H:%M:%S')+'</td><td>'+str(float(row[3]))+'</td></tr>'
        string += '</table>'
        self.finish(string)


class processing(web.RequestHandler):
    #@tornado.web.asynchronous
    def get(self, arg = None):
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
                self.write(escape.json_encode(sout))

                
            elif param['typ'] == 'RaDec2AltAz':
                # = loc.transform_to(AltAz(obstime = Time.now(), location=self.observatory))
                #F_az = (np.abs(self.horizont[:,0] - altaz.az.degree)).argmin()
                #local_horizont = self.horizont[F_az]
                pass




app = web.Application([
        (r'/', Overview),
        (r'/index', Overview),
        (r'/mount', Mount),
        (r'/observatory/weather/datatable', Obs_weather_datatable),
        (r'/observatory', Observatory),
        (r'/obs', Observatory),
        (r'/processing', processing),
        (r'/processing(.*)', processing),
       # (r'/multibolid(.*)', MultiBolid),
       # (r'/multibolid', MultiBolid),
       # (r'/realtime(.*)', RTbolidozor),
       # (r'/realtime', RTbolidozor),
       
        (r'/(favicon.ico)', web.StaticFileHandler, {'path': '.www/media/favicon.ico'}),
        (r'/fonts/(.*)', tornado.web.StaticFileHandler,{"path": './www/fonts/' }),
        (r"/(.*\.png)", tornado.web.StaticFileHandler,{"path": './www/media/' }),
        (r"/(.*\.jpg)", tornado.web.StaticFileHandler,{"path": './www/media/' }),
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