import psycopg2
from psycopg2.extras import RealDictCursor
import re


class Db:
	def __init__(self, name, usr, psw, ht):
		self.conn = psycopg2.connect(dbname = name, user=usr, 
                        password= psw, host = ht)
		self.conn.set_session(autocommit=True)
		self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
	def query(self, sql, params = []):
		if(len(params) > 0):
			for key in params.keys():
				sql = re.sub(":"+key, "%("+key+")s", sql)
			return self.cursor.execute(sql, params)
		else:
			return self.cursor.execute(sql)
	def row(self, sql, params=[]):
		self.query(sql, params)
		return self.cursor.fetchall()


# db = Db("encyclopedia", "postgres", "", '127.0.0.1')


# db.query("INSERT INTO specieses (image, name, description) VALUES (:image, :name, :des)", {"image": "qwdqwd", "name": 'Dsfrica', 'des': "dqwdqwdqw"})
# db.row("SELECT * FROM specieses")
# s = {"name": 'Africa', 'des': "adasd"}
# print(s['name'])


