from flask_restful import Resource, reqparse
from .domains import Domains
from db import Db

class Kinds(Resource):
	def get(self, id = 0):
		if(id != 0):
			kinds = self.db.row("SELECT * FROM kinds WHERE id = :id", {"id": id})
		else:
			kinds = self.db.row("SELECT * FROM kinds")
		if(len(kinds) > 0):
			answer = {"data": kinds, 'status': 200}
			return answer, 200
		else:
			answer = {"data": [], 'status': 404}
			return answer, 404
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name')
		parser.add_argument('domain_id')
		parser.add_argument('description')
		data = parser.parse_args()
		if(len(data) != 0):
			if(data['name'] is not None and data['domain_id'] is not None and data['description'] is not None):
				domain = Domains()
				dom_id = domain.get(data['domain_id'])[0]
				if(int(dom_id['status']) != 404):
					exist_name = self.db.row("SELECT name FROM kinds WHERE name = :name", {"name": data['name']})
					if(len(exist_name) == 0):
						kind_id = self.db.row("INSERT INTO kinds (name, domain_id, description) VALUES (:name, :domain_id, :description) RETURNING id", data)
						kind = self.db.row("SELECT * FROM kinds WHERE id = :id", kind_id[0])
						answer = {"data": kind, "status": 201}
						return answer, 201
					else:
						answer = {"data": "This name is exist", "status": 400}
						return answer, 400
				else:
					answer = {"data": "Bad request", "status": 400}
					return answer, 400
			else:
				answer = {"data": "Bad request", "status": 400}
				return answer, 400
		else:
			answer = {"data": "Bad request", "status": 400}
			return answer, 400
	def put(self, id):
		parser = reqparse.RequestParser()
		parser.add_argument('name')
		parser.add_argument('domain_id')
		parser.add_argument('description')
		data = parser.parse_args()
		data['id'] = id
		if(len(data) != 0 and id is not None):
			is_id = self.get(id)[0]
			if(is_id['status'] != 404):
				exist_name = self.db.row("SELECT name FROM kinds WHERE name = :name", {"name": data['name']})
				return exist_name
				if(len(exist_name) == 0):
					if(data['name'] is not None and data['domain_id'] is not None and data['description'] is not None):
						self.db.query("UPDATE kinds SET name = :name, domain_id = :domain_id, description = :description WHERE id = :id", data)
					elif(data['name'] is not None and data['domain_id'] is not None):
						self.db.query("UPDATE kinds SET name = :name, domain_id = :domain_id WHERE id = :id", data)
					elif(data['name'] is not None and data['description'] is not None):
						self.db.query("UPDATE kinds SET name = :name, description = :description WHERE id = :id", data)
					elif(data['domain_id'] is not None and data['description'] is not None):
						self.db.query("UPDATE kinds SET domain_id = :domain_id, description = :description WHERE id = :id", data)
					elif(data['name'] is not None):
						self.db.query("UPDATE kinds SET name = :name WHERE id = :id", data)
					elif(data['domain_id'] is not None):
						self.db.query("UPDATE kinds SET domain_id = :domain_id WHERE id = :id", data)
					elif(data['description'] is not None):
						self.db.query("UPDATE kinds SET description = :description WHERE id = :id", data)
					kind = self.db.row("SELECT * FROM kinds WHERE id = :id", {"id": id})
					answer = {"data": kind, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This name is exist", "status": 400}
					return answer, 400
			else:
				answer = {"data": "Bad request", "status": 400}
				return answer, 400
		else:
			answer = {"data": "Bad request", "status": 400}
			return answer, 400
	def delete(self, id):
		is_id = self.get(id)[0]
		if(is_id['status'] != 404):
			self.db.query("DELETE FROM kinds WHERE id = :id", {"id": id})
			answer = {"data": "Kind with id "+str(id)+" is deleted.", 'status': 200}
			return answer, 200
		else:
			answer = {"data": "Bad request", 'status': 400}
			return answer, 400