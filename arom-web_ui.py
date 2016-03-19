
#!/usr/bin/python
# -*- coding: utf-8 -*-

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


class Overview(web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, addres=None):
        print "web", addres
        self.render("www/layout/dash/publicOverview.html", title = "MyTitle")




app = web.Application([
        (r'/', Overview),
        (r'/index', Overview),
       # (r'/ws', SocketHandler),
       # (r'/clients', ClientsHandler),
       # (r'/multibolid(.*)', MultiBolid),
       # (r'/multibolid', MultiBolid),
       # (r'/realtime(.*)', RTbolidozor),
       # (r'/realtime', RTbolidozor),
       
        (r'/(favicon.ico)', web.StaticFileHandler, {'path': '.www/media/favicon.ico'}),
        (r"/(.*\.png)", tornado.web.StaticFileHandler,{"path": './www/media/' }),
        (r"/(.*\.jpg)", tornado.web.StaticFileHandler,{"path": './www/media/' }),
        (r"/(.*\.css)", tornado.web.StaticFileHandler,{"path": './www/css/' }),
        (r"/(.*\.wav)", tornado.web.StaticFileHandler,{"path": './www/wav/' }),
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