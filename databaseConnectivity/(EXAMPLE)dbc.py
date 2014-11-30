import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

class DatabaseController(object):
	def __init__(self, connection_address, connection_port, user_name, password, database):
		self.connection = mysql.connector.connect(host = connection_address, user=user_name, password = password, db = database)
		self.cursor = self.connection.cursor(buffered=True)
	
	def create_junk_table(self):
		query = "CREATE TABLE IF NOT EXISTS DPNET(why_mySQL int)"
		self.cursor.execute(query)
		self.connection.commit()

	def destroy_junk_table(self):
		query = "DROP TABLE IF EXISTS DPNET"
		self.cursor.execute(query)
		self.connection.commit()

	def create_users_table(self):
		query = "CREATE TABLE IF NOT EXISTS user(panther_id int Primary Key, password text)"
		self.cursor.execute(query)
		self.connection.commit()

	#ADDED by JIMMY
	def create_user(self, panther_id, password):
		query = "INSERT INTO user values(?, ?)"
		password = generate_password_hash(password)
		self.cursor.execute(query, (panther_id, password))
		self.connection.commit()

		#Added by Jimmy
	def check_credentials(self, panther_id, user_password):
		query = "SELECT password from user where panther_id = ?"
		self.cursor.execute(query, (panther_id))
		for password in self.cursor:
			return check_password_hash(password, user_password)#returns false if passwords dont match
		return false

#dbc = DatabaseController('localhost', 3306, 'testuser', 'test623', 'testdb')
#print(dbc)
#dbc.create_junk_table()