import tornado.ioloop, tornado.web, tornado.httpclient, os, json
from dbc import dbc

class BaseHandler(tornado.web.RequestHandler):

	def do_something(self):
		print("Self is required for all methods inside a class.  This defines THIS instance of the class(like this.methodName() in Java).  However, self is not necessarily injected inside the method when called.")

class MainHandler(BaseHandler):
	def get(self):
		dummy_value = 100
		self.render("index.html", dummy_value = dummy_value)

class SillyHandler(BaseHandler):
	def get(self, value_of_life):
		self.render("index.html", dummy_value = value_of_life)

def launch():
	handlers = [(r"/", MainHandler), (r"/(\w+)", SillyHandler)]
	server_settings = {"static_path": "./middleware/static", "template_path": "./middleware/templates", "login_url" : "/", "cookie_secret": os.urandom(24), "xsrf_cookies": True}
	application = tornado.web.Application(handlers, **server_settings)
	application.listen(8000, "localhost")
	#global database_controller
	#database_controller = dbc.DatabaseController("put your variables you need here")
	tornado.ioloop.IOLoop.instance().start()