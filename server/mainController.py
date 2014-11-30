import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import datetime
from databaseConnectivity import databaseController
from tornado.options import define, options
define("port", default=8000, help="run on specified port", type=int)

class BaseController(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("fullName")

class IndexController(BaseController):
    def get(self):
        reportList = databaseControl.get_top_reports()
        firstReport = reportList[0]
        secondReport = reportList[1]
        thirdReport = reportList[2]
        if (reportList[3] is not None):
        	fourthReport = reportList[3]
        else:
        	fourthReport = None
        if (reportList[4] is not None):
        	fifthReport = reportList[4]
        else:
        	fifthReport = None
        if (reportList[5] is not None):
        	sixthReport = reportList[5]
        else:
        	sixthReport = None
        if (reportList[6] is not None):
        	seventhReport = reportList[6]
        else:
        	seventhReport = None
        first = str(self.get_secure_cookie("Fname"))
        last = str(self.get_secure_cookie("Lname"))
        if (self.current_user is not None):
            username = first+" "+ last
            self.render('index.html', user = self.get_secure_cookie("fullName"), reportOne = firstReport, reportTwo = secondReport, reportThree = thirdReport, reportFour = fourthReport, reportFive = fifthReport, reportSix = sixthReport, reportSeven = seventhReport)
        else:
            self.render('index.html', user = None, reportOne = firstReport, reportTwo = secondReport, reportThree = thirdReport, reportFour = fourthReport, reportFive = fifthReport, reportSix = sixthReport, reportSeven = seventhReport)

'''class WebPageController(tornado.web.RequestHandler):'''
    #TODO: define this shit

class LoginController(BaseController):
    def post(self):
        usermail = self.get_argument("usermail")
        userpass = self.get_argument("password")
        if (databaseControl.verify_account(usermail, userpass)):
            userData = databaseControl.get_user(usermail)
            firstName = userData.First
            lastName = userData.Last
            userEmail = userData.Email
            userID = userData.ID
            userRole = userData.Role
            fullName = firstName + " " + lastName
            self.set_secure_cookie("fullName", fullName)
            self.set_secure_cookie("Fname", firstName)#passed from html with the tag username
            self.set_secure_cookie("Lname", lastName)
            self.set_secure_cookie("email", userEmail)
            self.set_secure_cookie("userID", str(userID))
            self.set_secure_cookie("userRole", str(userRole))
            self.redirect("/", permanent=True)
        else:
        	self.render('login.html', incorrect = True)
        '''TODO: return message stating password is incorrect and to try again'''
        #if PASSWORD is good, self.set_secure_cookie(username, self.get_argument("username"))
        #self.redirect("/", permanent=True)#if permanent = true, when user refreshes, more form data will NOT be sent
    def get(self):
        self.render('login.html', incorrect = False)#login.html page to be rendered
    '''def put(self):
        RETRIVE AND STORE USER DATA IN DATABASE'''
    class LogoutController(BaseController):
        @tornado.web.authenticated
        def get(self):
            self.clear_cookie("fullName")
            self.clear_cookie("Fname")#passed from html with the tag username
            self.clear_cookie("Lname")
            self.clear_cookie("email")
            self.clear_cookie("userID")
            self.clear_cookie("userRole")
            self.redirect("/")
            
        
#TODO: define this shit"""

class ReportController(BaseController):
    def get(self):
        self.render('report.html', userRole = int(self.get_secure_cookie("userRole")))
        
    class NewReportController(BaseController):
        @tornado.web.authenticated
        def get(self):
            self.render('create.html', user = self.current_user, userID = self.get_secure_cookie("userID"))
        def post(self):
            summary = self.get_argument("summary")
            description = self.get_argument("description")
            userID = int(self.get_secure_cookie("userID"))
            databaseControl.set_report(str(userID), summary, description)
            self.redirect("/", permanent = True)

class UserProfileController(BaseController):
    @tornado.web.authenticated
    def get(self):
        self.render('profile.html', fullName= self.get_secure_cookie("fullName"), firstName= self.get_secure_cookie("Fname"), lastName = self.get_secure_cookie("Lname"), userID = self.get_secure_cookie("userID"), userEmail = self.get_secure_cookie("email") )
    #TODO: define this shit
    
def launch():
    server_settings = {"static_path": os.path.join(os.path.dirname(__file__), "./static"), 
    "template_path": "./server/templates", 
    "login_url": "/login", 
    "cookie_secret": os.urandom(24)}

    handlers = [ (r'/', IndexController),
        (r'/report', ReportController),
        (r'/create', ReportController.NewReportController), 
        (r'/login', LoginController), 
        (r'/logout', LoginController.LogoutController),
        (r'/profile', UserProfileController) ]

    global databaseControl
    databaseControl = databaseController.DatabaseController('localhost', 3306, 'testuser', 'test623', 'testdb')

    application = tornado.web.Application(handlers, **server_settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()