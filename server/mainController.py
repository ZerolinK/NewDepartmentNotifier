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
        #gets top reports and populates entry in index.html, then renders it
        reportList = databaseControl.get_top_reports()
        firstReport = reportList[0]
        secondReport = reportList[1]
        thirdReport = reportList[2]
        if ((len(reportList) > 4) and (reportList[3] is not None)):
        	fourthReport = reportList[3]
        else:
        	fourthReport = None
        if ((len(reportList) > 5) and (reportList[4] is not None)):
        	fifthReport = reportList[4]
        else:
        	fifthReport = None
        if ((len(reportList) > 6) and (reportList[5] is not None)):
        	sixthReport = reportList[5]
        else:
        	sixthReport = None
        first = str(self.get_secure_cookie("Fname"))
        last = str(self.get_secure_cookie("Lname"))
        if (self.current_user is not None):
            username = first+" "+ last
            self.render('index.html', user = self.get_secure_cookie("fullName"), reportOne = firstReport, reportTwo = secondReport,
             reportThree = thirdReport, reportFour = fourthReport, reportFive = fifthReport, reportSix = sixthReport)
        else:
            self.render('index.html', user = None, reportOne = firstReport, reportTwo = secondReport, reportThree = thirdReport,
             reportFour = fourthReport, reportFive = fifthReport, reportSix = sixthReport)

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
            self.set_secure_cookie("Fname", firstName)
            self.set_secure_cookie("Lname", lastName)
            self.set_secure_cookie("email", userEmail)
            self.set_secure_cookie("userID", str(userID))
            self.set_secure_cookie("userRole", str(userRole))
            self.redirect("/", permanent=True)
        else:
        	self.render('login.html', incorrect = True)
    def get(self):
        self.render('login.html', incorrect = False)

    class LogoutController(BaseController):
        @tornado.web.authenticated
        def get(self):
            self.clear_cookie("fullName")
            self.clear_cookie("Fname")
            self.clear_cookie("Lname")
            self.clear_cookie("email")
            self.clear_cookie("userID")
            self.clear_cookie("userRole")
            self.render("logout.html")
            

class ViewController(BaseController):
    def get(self):
        #renders view of all reports, ranked by votes
        reportList = databaseControl.get_top_reports()
        self.render('view.html', fullName= self.get_secure_cookie("fullName"), reportList = reportList )

    class ReportController(BaseController):
        @tornado.web.authenticated
        def get(self, reportID):
            #renders view of selected report
            report = databaseControl.get_report(reportID)
            self.render('report.html', fullName = self.get_secure_cookie("fullName"), userRole = int(self.get_secure_cookie("userRole")), curReport = report, liked = False)
        @tornado.web.authenticated    
        def post(self, reportID, updateType):
		    #updates report based on user action
            update = int(updateType)
            if (update is 0):
			    #mark as solved
                databaseControl.mark_solved(reportID)
                report = databaseControl.get_report(reportID)
                self.render('report.html', fullName = self.get_secure_cookie("fullName"), userRole = int(self.get_secure_cookie("userRole")), curReport = report, liked = False)
            elif (update is 1):
                #add one more vote
                databaseControl.increment_vote(reportID)
                report = databaseControl.get_report(reportID)
                self.render('report.html', fullName = self.get_secure_cookie("fullName"), userRole = int(self.get_secure_cookie("userRole")), curReport = report, liked = True)

    class NewReportController(BaseController):
        @tornado.web.authenticated
        def get(self):
            #renders view of report creation template
            self.render('create.html', user = self.current_user, userID = self.get_secure_cookie("userID"))
        def post(self):
            #adds report from template into the database
            summary = self.get_argument("summary")
            description = self.get_argument("description")
            userID = int(self.get_secure_cookie("userID"))
            databaseControl.set_report(str(userID), summary, description)
            self.redirect("/", permanent = True)


class UserProfileController(BaseController):
    @tornado.web.authenticated
    def get(self):
        self.render('profile.html', fullName= self.get_secure_cookie("fullName"), firstName= self.get_secure_cookie("Fname"), lastName = self.get_secure_cookie("Lname"),
         userID = self.get_secure_cookie("userID"), userEmail = self.get_secure_cookie("email") )


def launch():
    server_settings = {"static_path": os.path.join(os.path.dirname(__file__), "./static"), 
    "template_path": "./server/templates", 
    "login_url": "/login", 
    "cookie_secret": os.urandom(24)}

    handlers = [ (r'/', IndexController),
        (r'/reports', ViewController),
        (r'/report/(.*)', ViewController.ReportController),
        (r'/(.*)/(.*)', ViewController.ReportController),
        (r'/create', ViewController.NewReportController), 
        (r'/login', LoginController), 
        (r'/logout', LoginController.LogoutController),
        (r'/profile', UserProfileController) ]

    global databaseControl
    databaseControl = databaseController.DatabaseController('localhost', 3306, 'testuser', 'test623', 'testdb')
    #databaseControl.create_basic_user("3654955", "Steve", "Ignetti", "signe001@fiu.edu", "dpnet")
    application = tornado.web.Application(handlers, **server_settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()