from flask_restful import Resource, reqparse
from .types import Types
from db import Db

class SubTypes(Resource):
	db = Db("encyclopedia", "postgres", "", '127.0.0.1')
	def get(self, id = 0):
		if(id != 0):
			sub_types = self.db.row("SELECT * FROM sub_types WHERE id = :id", {"id": id})
			types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE sub_type_id = :id", {'id': id})
			sub_types[0]['types'] = types
		else:
			sub_types = self.db.row("SELECT sub_types.* FROM sub_types")
			for sub_type in sub_types:
				types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE sub_type_id = :id", {'id': sub_type['id']})
				sub_type['types'] = types
				
		if(len(sub_types) > 0):
			answer = {"data": sub_types, 'status': 200}
			return answer, 200
		else:
			answer = {"data": [], 'status': 404}
			return answer, 404
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
		parser.add_argument('types_id', type=int, action='append', required=True, help="Type(s) id cannot be blank!")
		parser.add_argument('description', type=str, required=True, help="Description id cannot be blank!")
		data = parser.parse_args()
		exist_name = self.db.row("SELECT name FROM sub_types WHERE name = :name", {"name": data['name']})
		if(len(exist_name) == 0):
			types = Types()
			error = False
			for i in data['types_id']:
				type_id = types.get(i)[0]
				if(type_id['status'] == 404):
					error = True
					no_id = i
					break
			if(error is False):
				sub_type_id = self.db.row("INSERT INTO sub_types (name, description) VALUES (:name, :description) RETURNING id", data)
				sub_type = self.db.row("SELECT * FROM sub_types WHERE id = :id", sub_type_id[0])
				for i in data['types_id']:
					self.db.query("INSERT INTO types_sub_types (type_id, sub_type_id) VALUES (:type, :sub_type)", {"type": i, "sub_type": sub_type_id[0]['id']})
				types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE sub_type_id = :id", {'id': sub_type_id[0]['id']})
				sub_type[0]['types'] = types
				answer = {"data": sub_type, "status": 201}
				return answer, 201
			else:
				answer = {"data": "This id of types - "+str(no_id)+" not exist!", "status": 400}
				return answer, 400
		else:
			answer = {"data": "This name already exist!", "status": 400}
			return answer, 400
	def put(self, id):
		parser = reqparse.RequestParser()
		parser.add_argument('name')
		parser.add_argument('types_id', action='append')
		parser.add_argument('description')
		data = parser.parse_args()
		data['id'] = id
		is_id = self.get(id)[0]
		if(is_id['status'] != 404):
			if(data['name'] is not None and data['types_id'] is not None and data['description'] is not None):
				exist_name = self.db.row("SELECT name FROM sub_types WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE sub_types SET name = :name, description = :description WHERE id = :id", {'id': data['id'], 'name': data['name'], 'description': data['description']})
					self.db.query("DELETE FROM types_sub_types WHERE sub_type_id = :id", {"id": id})
					types = Types()
					error = False
					for i in data['types_id']:
						type_id = types.get(i)[0]
						if(type_id['status'] == 404):
							error = True
							no_id = i
							break
					if(error is False):
						sub_type = self.db.row("SELECT * FROM sub_types WHERE id = :id", {'id': id})
						for i in data['types_id']:
							self.db.query("INSERT INTO types_sub_types (type_id, sub_type_id) VALUES (:type, :sub_type)", {"type": i, "sub_type": id})
						types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE sub_type_id = :id", {'id': id})
						sub_type[0]['types'] = types
						answer = {"data": sub_type, "status": 201}
						return answer, 201
					else:
						answer = {"data": "This id of types - "+str(no_id)+" not exist!", "status": 400}
						return answer, 400
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
		
			elif(data['name'] is not None and data['types_id'] is not None):
				exist_name = self.db.row("SELECT name FROM sub_types WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE sub_types SET name = :name WHERE id = :id", {'id': data['id'], 'name': data['name']})
					self.db.query("DELETE FROM types_sub_types WHERE sub_type_id = :id", {"id": id})
					types = Types()
					error = False
					for i in data['types_id']:
						type_id = types.get(i)[0]
						if(type_id['status'] == 404):
							error = True
							no_id = i
							break
					if(error is False):
						sub_type = self.db.row("SELECT * FROM sub_types WHERE id = :id", {'id': id})
						for i in data['types_id']:
							self.db.query("INSERT INTO types_sub_types (type_id, sub_type_id) VALUES (:type, :sub_type)", {"type": i, "sub_type": id})
						types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE sub_type_id = :id", {'id': id})
						sub_type[0]['types'] = types
						answer = {"data": sub_type, "status": 201}
						return answer, 201
					else:
						answer = {"data": "This id of types - "+str(no_id)+" not exist!", "status": 400}
						return answer, 400
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
			elif(data['name'] is not None and data['description'] is not None):
				exist_name = self.db.row("SELECT name FROM sub_types WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE sub_types SET name = :name, description = :description WHERE id = :id", {'id': data['id'], 'name': data['name'], 'description': data['description']})
					sub_type = self.db.row("SELECT * FROM sub_types WHERE id = :id", {'id': id})
					types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE sub_type_id = :id", {'id': id})
					sub_type[0]['types'] = types
					answer = {"data": sub_type, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
			elif(data['types_id'] is not None and data['description'] is not None):
				self.db.query("UPDATE sub_types SET description = :description WHERE id = :id", {'id': data['id'], 'description': data['description']})
				self.db.query("DELETE FROM types_sub_types WHERE sub_type_id = :id", {"id": id})
				types = Types()
				error = False
				for i in data['types_id']:
					type_id = types.get(i)[0]
					if(type_id['status'] == 404):
						error = True
						no_id = i
						break
				if(error is False):
					sub_type = self.db.row("SELECT * FROM sub_types WHERE id = :id", {'id': id})
					for i in data['types_id']:
						self.db.query("INSERT INTO types_sub_types (type_id, sub_type_id) VALUES (:type, :sub_type)", {"type": i, "sub_type": id})
					types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE sub_type_id = :id", {'id': id})
					sub_type[0]['types'] = types
					answer = {"data": sub_type, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This id of types - "+str(no_id)+" not exist!", "status": 400}
					return answer, 400
			elif(data['types_id'] is not None):
				self.db.query("DELETE FROM types_sub_types WHERE sub_type_id = :id", {"id": id})
				types = Types()
				error = False
				for i in data['types_id']:
					type_id = types.get(i)[0]
					if(type_id['status'] == 404):
						error = True
						no_id = i
						break
				if(error is False):
					sub_type = self.db.row("SELECT * FROM sub_types WHERE id = :id", {'id': id})
					for i in data['types_id']:
						self.db.query("INSERT INTO types_sub_types (type_id, sub_type_id) VALUES (:type, :sub_type)", {"type": i, "sub_type": id})
					types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE sub_type_id = :id", {'id': id})
					sub_type[0]['types'] = types
					answer = {"data": sub_type, "status": 201}
					return answer, 201
			elif(data['name'] is not None):
				exist_name = self.db.row("SELECT name FROM sub_types WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE sub_types SET name = :name WHERE id = :id", {'id': data['id'], 'name': data['name']})
					types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE sub_type_id = :id", {'id': id})
					sub_type[0]['types'] = types
					answer = {"data": sub_type, "status": 201}
					return answer, 201
			elif(data['description'] is not None):
				self.db.query("UPDATE sub_types SET description = :description WHERE id = :id", {'id': data['id'], 'description': data['description']})
				types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE sub_type_id = :id", {'id': id})
				sub_type[0]['types'] = types
				answer = {"data": sub_type, "status": 201}
				return answer, 201
		else:
			answer = {"data": "Bad request", 'status': 400}
	def delete(self, id):
		is_id = self.get(id)[0]
		if(is_id['status'] != 404):
			self.db.query("DELETE FROM sub_types WHERE id = :id; DELETE FROM types_sub_types WHERE sub_type_id = :id", {"id": id})
			answer = {"data": "Sub Type with id "+str(id)+" is deleted.", 'status': 200}
			return answer, 200
		else:
			answer = {"data": "Bad request", 'status': 400}
			return answer, 400
