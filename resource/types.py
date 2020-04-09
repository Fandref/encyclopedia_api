from flask_restful import Resource, reqparse
from .kinds import Kinds
from db import Db

class Types(Resource):
	db = Db("encyclopedia", "postgres", "", '127.0.0.1')
	def get(self, id = 0):
		if(id != 0):
			types = self.db.row("SELECT * FROM types WHERE id = :id", {"id": id})
		else:
			types = self.db.row("SELECT * FROM types")
		if(len(types) > 0):
			answer = {"data": types, 'status': 200}
			return answer, 200
		else:
			answer = {"data": [], 'status': 404}
			return answer, 404
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name')
		parser.add_argument('kind_id')
		parser.add_argument('description')
		data = parser.parse_args()
		if(len(data) != 0):
			if(data['name'] is not None and data['kind_id'] is not None and data['description'] is not None):
				kind = Kinds()
				kind_id = kind.get(data['kind_id'])[0]
				if(int(kind_id['status']) != 404):
					exist_name = self.db.row("SELECT name FROM types WHERE name = :name", {"name": data['name']})
					if(len(exist_name) == 0):
						type_id = self.db.row("INSERT INTO types (name, kind_id, description) VALUES (:name, :kind_id, :description) RETURNING id", data)
						type = self.db.row("SELECT * FROM types WHERE id = :id", type_id[0])
						answer = {"data": type, "status": 201}
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
		parser.add_argument('kind_id')
		parser.add_argument('description')
		data = parser.parse_args()
		data['id'] = id
		if(id is not None):
			is_id = self.get(id)[0]
			if(is_id['status'] != 404):
				exist_name = self.db.row("SELECT name FROM types WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					if(data['name'] is not None and data['kind_id'] is not None and data['description'] is not None):
						self.db.query("UPDATE types SET name = :name, kind_id = :kind_id, description = :description WHERE id = :id", data)
					elif(data['name'] is not None and data['kind_id'] is not None):
						self.db.query("UPDATE types SET name = :name, kind_id = :kind_id WHERE id = :id", data)
					elif(data['name'] is not None and data['description'] is not None):
						self.db.query("UPDATE types SET name = :name, description = :description WHERE id = :id", data)
					elif(data['kind_id'] is not None and data['description'] is not None):
						self.db.query("UPDATE types SET kind_id = :kind_id, description = :description WHERE id = :id", data)
					elif(data['name'] is not None):
						self.db.query("UPDATE types SET name = :name WHERE id = :id", data)
					elif(data['kind_id'] is not None):
						self.db.query("UPDATE types SET kind_id = :kind_id WHERE id = :id", data)
					elif(data['description'] is not None):
						self.db.query("UPDATE types SET description = :description WHERE id = :id", data)
					types = self.db.row("SELECT * FROM types WHERE id = :id", {"id": id})
					answer = {"data": types, "status": 201}
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
			self.db.query("DELETE FROM types WHERE id = :id", {"id": id})
			answer = {"data": "Type with id "+str(id)+" is deleted.", 'status': 200}
			return answer, 200
		else:
			answer = {"data": "Bad request", 'status': 400}
			return answer, 400