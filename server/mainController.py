import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on specified port", type=int)


class BaseController(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

    #TODO: define this shit

class IndexController(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')#, user=self.current_user)
    #TODO: define this shit

#class WebPageController(tornado.web.RequestHandler):
    #TODO: define this shit

class LoginController(tornado.web.RequestHandler):
    def post(self):
        self.set_secure_cookie("username", self.get_argument("username"))#passed from html with the tag username
        self.redirect("/")
    def get(self):
        self.render('login.html')#login.html page to be rendered

    class LogoutController(BaseController):
        def get(self):
            if (self.get_argument("logout", None)):
                self.clear_cookie("username")
                self.redirect("/")
    #TODO: define this shit"""

class ReportController(BaseController):
    @tornado.web.authenticated#this requires that auser be logged in to see
    def get(self):
        self.render('report.html')
#    def post(self):
        #put appropriate fetches from template here and send to database
#class UserProfileController(BaseController):
    #TODO: define this shit
def launch():
    server_settings = {"static_path": os.path.join(os.path.dirname(__file__), "./static"), 
    "template_path": "./server/templates", 
    "login_url": "/login", 
    "cookie_secret": os.urandom(24), 
    "xsrf_cookies": True}

    handlers = [ (r'/', IndexController),
        (r'/report', ReportController), 
        (r'/login', LoginController), 
        (r'/logout', LoginController.LogoutController) ]
    
    application = tornado.web.Application(handlers, **server_settings)
    #application.listen(port, localhost)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()