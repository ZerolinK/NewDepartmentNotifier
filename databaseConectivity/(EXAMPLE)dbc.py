import mysql.connector

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
		self.connection.execute(query)
		self.connection.commit()

#dbc = DatabaseController('localhost', 3306, 'testuser', 'test623', 'testdb')
#print(dbc)
#dbc.create_junk_table()