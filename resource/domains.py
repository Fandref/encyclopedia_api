from flask_restful import Resource, reqparse
from db import Db

class Domains(Resource):
	db = Db("encyclopedia", "postgres", "", '127.0.0.1')
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name')
		parser.add_argument('description')
		data = parser.parse_args()
		if(len(data) != 0):
			if(data['name'] is not None and data['description'] is not None):
				domain_id = self.db.row("INSERT INTO domains (name, description) VALUES (:name, :description) RETURNING id", data)
				domain = self.db.row("SELECT * FROM domains WHERE id = :id", domain_id[0])
				answer = {"data": domain, "status": 201}
				return answer, 201
			else:
				answer = {"data": "Bad request", "status": 400}
				return answer, 400
		else:
			answer = {"data": "Bad request", "status": 400}
			return answer, 400
	def get(self, id = 0):
		if(id != 0):
			domain = self.db.row("SELECT * FROM domains WHERE id = :id", {"id": id})
		else:
			domain = self.db.row("SELECT * FROM domains")
		if(len(domain) > 0):
			answer = {"data": domain, 'status': 200}
			return answer, 200
		else:
			answer = {"data": [], 'status': 404}
			return answer, 404
	def put(self, id):
		parser = reqparse.RequestParser()
		parser.add_argument('name')
		parser.add_argument('description')
		data = parser.parse_args()
		data['id'] = id
		if(len(data) != 0 and id is not None):
			is_id = self.get(id)[0]
			if(is_id['status'] != 404):
				if(data['description'] is not None and data['name'] is not None):
					self.db.query("UPDATE domains SET name = :name, description = :description WHERE id = :id", data)
				if(data['name'] is not None):
					self.db.query("UPDATE domains SET name = :name WHERE id = :id", data)
				elif(data['description'] is not None):
					self.db.query("UPDATE domains SET description = :description WHERE id = :id", data)
				domain = self.db.row("SELECT * FROM domains WHERE id = :id", {"id": id})
				answer = {"data": domain, "status": 201}
				return answer, 201
			else:
				answer = {"data": "Bad request", 'status': 400}
				return "Bad request", 400
		else:
			answer = {"data": "Bad request", 'status': 400}
			return "Bad request", 400
	def delete(self, id):
		is_id = self.get(id)[0]
		if(is_id['status'] != 404):
			self.db.query("DELETE FROM domains WHERE id = :id", {"id": id})
			return f"World area with id {id} is deleted.", 200
		else:
			answer = {"data": "Bad request", 'status': 400}
			return "Bad request", 400