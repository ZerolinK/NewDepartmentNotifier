import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class Report(object):
        def __init__(self, ReportID, UserID, Summary, Description, Votes, Is_resolved, Date):
                self.reportID = ReportID
                self.userID = UserID
                self.summary = Summary
                self.description = Description
                self.votes = Votes
                self.resolved = Is_resolved
                self.date = Date
        def make_new_report(UserID, Summary, Description, Votes, Is_resolved, Date):
                report = Report(0, UserID, Summary, Description, Votes, Is_resolved, Date)
                return report

        def make_report(ReportID, UserID, Summary, Description, Votes, Is_resolved, Date):
                report = Report(ReportID, UserID, Summary, Description, Votes, Is_resolved, Date)
                return report

class User(object):
        def __init__(self, FirstName, LastName, UserID, Email, Role):
                self.First = FirstName
                self.Last = LastName
                self.ID = UserID
                self.Email = Email
                self.Role = Role
        def make_user(FirstName, LastName, UserID, Email, Role):
                user = User(FirstName, LastName, UserID, Email, Role)
                return user

class DatabaseController(object):
        def __init__(self, connection_address, connection_port, user_name, password, database):
                self.connection = mysql.connector.connect(host = connection_address, user=user_name, password = password, db = database)
                self.cursor = self.connection.cursor(buffered=True)
        def create_table(self):
                query = "CREATE TABLE IF NOT EXISTS DPNET(why_mySQL int)"
                self.cursor.execute(query)
                self.connection.commit()
        def destroy_table(self):
                query = "DROP TABLE IF EXISTS DPNET"
                self.cursor.execute(query)
                self.connection.commit()

        def verify_account(self, email, user_password):
                #query = "SELECT Pass FROM user WHERE Email = '" + email +"'"
                query = "SELECT Pass FROM user WHERE Email = %s"
                self.cursor.execute(query, (email, ))
                fetch = self.cursor.fetchone()
                password = " ".join(map(str, fetch))
                return check_password_hash(password, user_password)

        def set_report(self, userID, summary, description):
                #query = "INSERT INTO `testdb`.`report` (`Report_ID`, `User_ID`, `Summary`, `Description`, `Votes`, `Is_Resolved`) VALUES ('" + reportID + "', '" + userID + "', '" + summary + "', '" + description + "', '0', '0')"
                query = "INSERT INTO `testdb`.`report` ( `User_ID`, `Summary`, `Description`, `Votes`, `Is_Resolved` ) VALUES ( %s, %s, %s, '0', '0')"
                self.cursor.execute(query, (userID, summary, description))
                self.connection.commit()

        def increment_vote(self, reportID):
                #query1 = "SELECT Votes FROM report WHERE Report_ID = '" + reportID +"'"
                query1 = "SELECT Votes FROM report WHERE Report_ID = %s"
                self.cursor.execute(query1, (reportID, ))
                fetch = self.cursor.fetchone()
                curVote = " ".join(map(str, fetch))
                intVote = int(curVote)
                intVote = intVote + 1
                newVote= str(intVote)
                #query2 = "UPDATE `testdb`.`report` SET `Votes` = '" + str(intVote) + "' WHERE `report`.`Report_ID` = " + reportID
                query2 = "UPDATE `testdb`.`report` SET `Votes` = %s WHERE `report`.`Report_ID` = %s"
                self.cursor.execute(query2, (newVote, reportID))
                self.connection.commit()

        def mark_solved(self, reportID):
                fetch = self.cursor.fetchone()
                curVote = " ".join(map(str, fetch))
                resolved = "1"
                query = "UPDATE `testdb`.`report` SET `Is_Resolved` = %s WHERE `report`.`Report_ID` = %s"
                self.cursor.execute(query, (resolved ,reportID, ))
                self.connection.commit()

        def get_vote(self, reportID):
                #query1 = "SELECT Votes FROM report WHERE Report_ID = '" + reportID +"'"
                query1 = "SELECT Votes FROM report WHERE Report_ID = %s"
                self.cursor.execute(query1, (reportID, ))
                fetch = self.cursor.fetchone()
                curVote = " ".join(map(str, fetch))
                intVote = int(curVote)
                return intVote

        def resolve_issue(self, reportID):
                #query = "UPDATE `testdb`.`report` SET `Is_Resolved` = '1' WHERE `report`.`Report_ID` = " + reportID
                query = "UPDATE `testdb`.`report` SET `Is_Resolved` = '1' WHERE `report`.`Report_ID` = %s"
                self.cursor.execute(query, (reportID, ))
                self.connection.commit()

        def create_report(self, newReport):
                query = "INSERT INTO `testdb`.`report` (`Report_ID`, `User_ID`, `Summary`, `Description`, `Votes`, `Is_Resolved`, `Date`) VALUES (null, %s, %s, %s, '0', '0', CURRENT_TIMESTAMP)"
                userID = str(newReport.userID)
                summary = newReport.summary
                description = newReport.description
                print(userID)
                print(summary)
                print(description)
                self.cursor.execute(query, (userID, summary, description))
                self.connection.commit 

        def get_report(self, reportID): 
                query = "SELECT * FROM report WHERE Report_ID = %s"
                self.cursor.execute(query, (reportID, ))
                for(Report_ID, User_ID, Summary, Description, Votes, Is_Resolved, Date) in self.cursor:
                        print(Report_ID)
                        print(User_ID)
                        print(Summary)
                        reportData = Report.make_report(Report_ID, User_ID, Summary, Description, Votes, Is_Resolved, Date)
                self.connection.commit()
                return reportData

        def get_top_reports(self):
                query = "SELECT * FROM `report` ORDER BY `report`.`Votes` DESC "
                self.cursor.execute(query)
                reportList = []
                for (Report_ID, User_ID, Summary, Description, Votes, Is_Resolved, Date) in self.cursor:
                        reportData = Report.make_report(Report_ID, User_ID, Summary, Description, Votes, Is_Resolved, Date)
                        reportList.append(reportData)
                return reportList

        def create_basic_user(self, userID, fName, lName, email, password):
                password2 = generate_password_hash(password)
                #query = "INSERT INTO `testdb`.`user` (`ID`, `FName`, `LName`, `Email`, `Pass`, `Role`) VALUES ('" + userID + "', '" + fName + "', '" + lName + "', '" + email +"', '" + password2 + "', '0')"
                query = "INSERT INTO `testdb`.`user` (`ID`, `FName`, `LName`, `Email`, `Pass`, `Role`) VALUES (%s, %s, %s, %s, %s, '0')"
                self.cursor.execute(query, (userID, fName, lName, email, password2))
                self.connection.commit()

        def get_user(self, userMail):
                query = "SELECT Fname, LName, Email, ID, Role FROM user WHERE EMail = %s"
                self.cursor.execute(query, (userMail, ))
                for (FName, LName, Email, ID, Role) in self.cursor:
                        curUser = User.make_user(FName, LName, ID, Email, Role)
                self.connection.commit()
                return curUser

        def create_faculty_user(self, userID, fName, lName, email, password):
                password2 = generate_password_hash(password)
                #query = "INSERT INTO `testdb`.`user` (`ID`, `FName`, `LName`, `Email`, `Pass`, `Role`) VALUES ('" + userID + "', '" + fName + "', '" + lName + "', '" + email +"', '" + password2 + "', '1')"
                query = "INSERT INTO `testdb`.`user` (`ID`, `FName`, `LName`, `Email`, `Pass`, `Role`) VALUES (%s, %s, %s, %s, %s, '1')"
                self.cursor.execute(query, (userID, fName, lName, email, password2))
                self.connection.commit()
        
        def close_connection(self):
                self.connection.close()

        
#dbc = DatabaseController('localhost', 3306, 'testuser', 'test623', 'testdb')
#dbc.create_basic_user("1586390", "Daniel", "Gonzalez", "dgonz023@fiu.edu", "dpnet")
#print(dbc.verify_account("dgonz023@fiu.edu", "dpnet"))

