from flask_restful import Resource, reqparse
from .sub_types import SubTypes
from db import Db

class Classes(Resource):
	db = Db("encyclopedia", "postgres", "", '127.0.0.1')
	def get(self, id = 0):
		if(id != 0):
			classes = self.db.row("SELECT * FROM classes WHERE id = :id", {"id": id})
			sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE class_id = :id", {'id': id})
			classes[0]['sub_types'] = sub_types
		else:
			classes = self.db.row("SELECT * FROM classes")
			for cl in classes:
				sub_type = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE class_id = :id", {'id': cl['id']})
				cl['sub_types'] = sub_type			
		if(len(classes) > 0):
			answer = {"data": classes, 'status': 200}
			return answer, 200
		else:
			answer = {"data": [], 'status': 404}
			return answer, 404
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
		parser.add_argument('sub_types_id', type=int, action='append', required=True, help="Type(s) id cannot be blank!")
		parser.add_argument('description', type=str, required=True, help="Description id cannot be blank!")
		data = parser.parse_args()
		exist_name = self.db.row("SELECT name FROM classes WHERE name = :name", {"name": data['name']})
		if(len(exist_name) == 0):
			sub_types = SubTypes()
			error = False
			for i in data['sub_types_id']:
				sub_type_id = sub_types.get(i)[0]
				if(sub_type_id['status'] == 404):
					error = True
					no_id = i
					break
			if(error is False):
				class_id = self.db.row("INSERT INTO classes (name, description) VALUES (:name, :description) RETURNING id", data)
				cl = self.db.row("SELECT * FROM classes WHERE id = :id", class_id[0])
				for i in data['sub_types_id']:
					self.db.query("INSERT INTO sub_types_classes (sub_type_id, class_id) VALUES (:sub_type, :class_id)", {"sub_type": i, "class_id": cl[0]['id']})
				sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE class_id = :id", {'id': cl[0]['id']})
				cl[0]['sub_types'] = sub_types
				answer = {"data": cl, "status": 201}
				return answer, 201
			else:
				answer = {"data": "This id of sub type - "+str(no_id)+" not exist!", "status": 400}
				return answer, 400
		else:
			answer = {"data": "This name already exist!", "status": 400}
			return answer, 400
	def put(self, id):
		parser = reqparse.RequestParser()
		parser.add_argument('name')
		parser.add_argument('sub_types_id', action='append')
		parser.add_argument('description')
		data = parser.parse_args()
		data['id'] = id
		is_id = self.get(id)[0]
		if(is_id['status'] != 404):
			if(data['name'] is not None and data['sub_types_id'] is not None and data['description'] is not None):
				exist_name = self.db.row("SELECT name FROM classes WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE classes SET name = :name, description = :description WHERE id = :id", {'id': data['id'], 'name': data['name'], 'description': data['description']})
					self.db.query("DELETE FROM sub_types_classes WHERE class_id = :id", {"id": id})
					sub_type = SubTypes()
					error = False
					for i in data['sub_types_id']:
						sub_type_id = sub_type.get(i)[0]
						if(sub_type_id['status'] == 404):
							error = True
							no_id = i
							break
					if(error is False):
						cl = self.db.row("SELECT * FROM classes WHERE id = :id", {'id': id})
						for i in data['sub_types_id']:
							self.db.query("INSERT INTO sub_types_classes (sub_type_id, class_id) VALUES (:sub_type, :class_id)", {"sub_type": i, "class_id": id})
						sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE class_id = :id", {'id': id})
						cl[0]['sub_types'] = sub_types
						answer = {"data": cl, "status": 201}
						return answer, 201
					else:
						answer = {"data": "This id of sub types - "+str(no_id)+" not exist!", "status": 400}
						return answer, 400
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
		
			elif(data['name'] is not None and data['sub_types_id'] is not None):
				exist_name = self.db.row("SELECT name FROM classes WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE classes SET name = :name WHERE id = :id", {'id': data['id'], 'name': data['name']})
					self.db.query("DELETE FROM sub_types_classes WHERE class_id = :id", {"id": id})
					sub_type = SubTypes()
					error = False
					for i in data['sub_types_id']:
						sub_type_id = sub_type.get(i)[0]
						if(sub_type_id['status'] == 404):
							error = True
							no_id = i
							break
					if(error is False):
						cl = self.db.row("SELECT * FROM classes WHERE id = :id", {'id': id})
						for i in data['types_id']:
							self.db.query("INSERT INTO sub_types_classes (sub_type_id, :class_id) VALUES (:sub_type, :class_id)", {"sub_type": i, "class_id": id})
						sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE class_id = :id", {'id': id})
						cl[0]['sub_types'] = sub_types
						answer = {"data": cl, "status": 201}
						return answer, 201
					else:
						answer = {"data": "This id of sub type - "+str(no_id)+" not exist!", "status": 400}
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
			elif(data['sub_types_id'] is not None and data['description'] is not None):
				self.db.query("UPDATE classes SET description = :description WHERE id = :id", {'id': data['id'], 'description': data['description']})
				self.db.query("DELETE FROM sub_types_classes WHERE class_id = :id", {"id": id})
				sub_type = SubTypes()
				error = False
				for i in data['sub_types_id']:
					sub_type_id = sub_type.get(i)[0]
					if(sub_type_id['status'] == 404):
						error = True
						no_id = i
						break
				if(error is False):
					cl = self.db.row("SELECT * FROM classes WHERE id = :id", {'id': id})
					for i in data['sub_types_id']:
						self.db.query("INSERT INTO sub_types_classes (sub_type_id, class_id) VALUES (:sub_type, :class_id)", {"sub_type": i, "class_id": id})
					sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE class_id = :id", {'id': id})
					cl[0]['sub_types'] = sub_types
					answer = {"data": cl, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This id of sub types - "+str(no_id)+" not exist!", "status": 400}
					return answer, 400
			elif(data['sub_types_id'] is not None):
				self.db.query("DELETE FROM sub_types_classes WHERE class_id = :id", {"id": id})
				sub_type = SubTypes()
				error = False
				for i in data['sub_types_id']:
					sub_type_id = sub_type.get(i)[0]
					if(sub_type_id['status'] == 404):
						error = True
						no_id = i
						break
				if(error is False):
					cl = self.db.row("SELECT * FROM classes WHERE id = :id", {'id': id})
					for i in data['sub_types_id']:
						self.db.query("INSERT INTO sub_types_classes (sub_type_id, class_id) VALUES (:sub_type, :class_id)", {"sub_type": i, "class_id": id})
					sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE class_id = :id", {'id': id})
					cl[0]['sub_types'] = sub_types
					answer = {"data": cl, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This id of sub types - "+str(no_id)+" not exist!", "status": 400}
					return answer, 400
			elif(data['name'] is not None):
				exist_name = self.db.row("SELECT name FROM classes WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE classes SET name = :name WHERE id = :id", {'id': data['id'], 'name': data['name']})
					cl = self.db.row("SELECT * FROM classes WHERE id = :id", {"id": id})
					sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE class_id = :id", {'id': id})
					cl[0]['sub_types'] = sub_types
					answer = {"data": cl, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
			elif(data['description'] is not None):
				self.db.query("UPDATE classes SET description = :description WHERE id = :id", {'id': data['id'], 'description': data['description']})
				cl = self.db.row("SELECT * FROM classes WHERE id = :id", {"id": id})
				sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE class_id = :id", {'id': id})
				cl[0]['sub_types'] = sub_types
				answer = {"data": cl, "status": 201}
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