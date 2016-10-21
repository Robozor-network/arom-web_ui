import os
import tornado.ioloop
import tornado.web
import rospy
import rosnode


'''
export ROS_HOSTNAME=roman-notebook
export ROS_MASTER_URI=http://arom-weather.local:11311
export ROS_IP=roman-notebook.local

'''


def NodeList():
	return rosnode.get_node_names()

permanent = {'nodeList': NodeList()}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #self.write("Hello, world")
        self.render("home.html", entries=['bla','bla2', 'test3'], permanent=permanent)


class NodeHandler(tornado.web.RequestHandler):
    def get(self, node):
        #self.write("Hello, world" + str(node))
        try:
        	self.render("node.html", node=node, nodeParam=rospy.get_param('/arom/node'+node+'/'), permanent=permanent)
        except Exception, e:
        	self.write("Na teto strance neni neco v poradku")

def make_app():
    return tornado.web.Application([
        (r"/node/(.*)", NodeHandler),
        (r"/", MainHandler),
    ],
    debug= True,
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()