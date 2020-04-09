from flask_restful import Resource, reqparse
from .classes import Classes as Cls
from db import Db

class SubClasses(Resource):
	db = Db("encyclopedia", "postgres", "", '127.0.0.1')

	def get(self, id = 0):
		if (id != 0 ): 
			sub_classes = self.db.row("SELECT * FROM sub_classes WHERE id = :id", {"id": id})
			if(len(sub_classes) > 0):
				sub_classes[0]['classes'] = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE classes_sub_classes.sub_class_id = :id", {'id': id})
				sub_classes[0]['sub_types'] = []
				sub_classes[0]['types'] = []
				sub_classes[0]['kinds'] = []
				sub_classes[0]['domains'] = []
				for clas in sub_classes[0]['classes']:
					sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE sub_types_classes.class_id = :id GROUP BY sub_types.id", {'id': clas['id']})
					for sub_type in sub_types:
						if sub_type not in sub_classes[0]['sub_types']:
							sub_classes[0]['sub_types'].append(sub_type)
				for sub_type in sub_classes[0]['sub_types']:
					types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE types_sub_types.sub_type_id = :id GROUP BY types.id", {'id': sub_type['id']})
					for type in types:
						if type not in sub_classes[0]['types']:
							sub_classes[0]['types'].append(type)
				for type in sub_classes[0]['types']:
					kinds = self.db.row("SELECT kinds.id, kinds.name FROM types RIGHT JOIN kinds ON types.kind_id = kinds.id WHERE types.id = :id GROUP BY kinds.id", {'id': type['id']})
					for kind in kinds:
						if kind not in sub_classes[0]['kinds']:
							sub_classes[0]['kinds'].append(kind)
				for kind in sub_classes[0]['kinds']:
					domains = self.db.row("SELECT domains.id, domains.name FROM kinds RIGHT JOIN domains ON kinds.domain_id = domains.id WHERE kinds.id = :id GROUP BY domains.id", {'id': kind['id']})
					for domain in domains:
						if domain not in sub_classes[0]['domains']:
							sub_classes[0]['domains'].append(domain)	
		else:
			parser = reqparse.RequestParser()
			ordparser = reqparse.RequestParser()
			parser.add_argument('domains', type=int)
			parser.add_argument('kinds', type=int)
			parser.add_argument('types', type=int)
			parser.add_argument('sub_types', type=int)
			parser.add_argument('classes', type=int)
			data = parser.parse_args()
			ordparser.add_argument('order', type=str)
			order = ordparser.parse_args()['order']
			filters = dict(filter(lambda elem: elem[1] is not None, data.items()))
			if(order is None):
				sub_classes = self.db.row("SELECT * FROM sub_classes")
			elif(order == 'ASC'):
				sub_classes = self.db.row("SELECT * FROM sub_classes ORDER BY name ASC")
			elif(order == 'DESC'):
				sub_classes = self.db.row("SELECT * FROM sub_classes ORDER BY name DESC")
			else:
				sub_classes = self.db.row("SELECT * FROM sub_classes")
			for sub_class in sub_classes:
				sub_class['classes'] = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE sub_class_id = :id", {'id': sub_class['id']})
				sub_class['sub_types'] = []
				sub_class['types'] = []
				sub_class['kinds'] = []
				sub_class['domains'] = []
				for clas in sub_class['classes']:
					sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE sub_types_classes.class_id = :id GROUP BY sub_types.id", {'id': clas['id']})
					for sub_type in sub_types:
						if sub_type not in sub_class['sub_types']:
							sub_class['sub_types'].append(sub_type)
				for sub_type in sub_class['sub_types']:
					types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE types_sub_types.sub_type_id = :id GROUP BY types.id", {'id': sub_type['id']})
					for type in types:
						if type not in sub_class['types']:
							sub_class['types'].append(type)
				for type in sub_class['types']:
					kinds = self.db.row("SELECT kinds.id, kinds.name FROM types RIGHT JOIN kinds ON types.kind_id = kinds.id WHERE types.id = :id GROUP BY kinds.id", {'id': type['id']})
					for kind in kinds:
						if kind not in sub_class['kinds']:
							sub_class['kinds'].append(kind)
				for kind in sub_class['kinds']:
					domains = self.db.row("SELECT domains.id, domains.name FROM kinds RIGHT JOIN domains ON kinds.domain_id = domains.id WHERE kinds.id = :id GROUP BY domains.id", {'id': kind['id']})
					for domain in domains:
						if domain not in sub_class['domains']:
							sub_class['domains'].append(domain)	
			for filter_name, filter_val in filters.items():
				for sub_class in sub_classes:
					for s in sub_class[filter_name]:
						if(filter_val != s['id']):
							sub_classes.remove(sub_class)
		if(len(sub_classes) > 0):
			answer = {"data": sub_classes, 'status': 200}
			return answer, 200
		else:
			answer = {"data": [], 'status': 404}
			return answer, 404

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
		parser.add_argument('classes_id', type=int, action='append', required=True, help="Type(s) id cannot be blank!")
		parser.add_argument('description', type=str, required=True, help="Description id cannot be blank!")
		data = parser.parse_args()
		exist_name = self.db.row("SELECT name FROM sub_classes WHERE name = :name", {"name": data['name']})
		if(len(exist_name) == 0):
			classes = Cls()
			error = False
			for i in data['classes_id']:
				class_id = classes.get(i)[0]
				if(class_id['status'] == 404):
					error = True
					no_id = i
					break
			if(error is False):
				sub_class_id = self.db.row("INSERT INTO sub_classes (name, description) VALUES (:name, :description) RETURNING id", data)
				sub_class= self.db.row("SELECT * FROM sub_classes WHERE id = :id", sub_class_id[0])
				for i in data['classes_id']:
					self.db.query("INSERT INTO classes_sub_classes (class_id, sub_class_id) VALUES (:class, :sub_class_id)", {"class": i, "sub_class_id": sub_class[0]['id']})
				classes = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE sub_class_id = :id", {'id': sub_class[0]['id']})
				sub_class[0]['classes'] = classes
				answer = {"data": sub_class, "status": 201}
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
		parser.add_argument('classes_id', action='append')
		parser.add_argument('description')
		data = parser.parse_args()
		data['id'] = id
		is_id = self.get(id)[0]
		if(is_id['status'] != 404):
			if(data['name'] is not None and data['classes_id'] is not None and data['description'] is not None):
				exist_name = self.db.row("SELECT name FROM sub_classes WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE sub_classes SET name = :name, description = :description WHERE id = :id", {'id': data['id'], 'name': data['name'], 'description': data['description']})
					self.db.query("DELETE FROM classes_sub_classes WHERE sub_class_id = :id", {"id": id})
					clas = Cls()
					error = False
					for i in data['classes_id']:
						class_id = clas.get(i)[0]
						if(class_id['status'] == 404):
							error = True
							no_id = i
							break
					if(error is False):
						sub_class= self.db.row("SELECT * FROM sub_classes WHERE id = :id", {'id': id})
						for i in data['classes_id']:
							self.db.query("INSERT INTO classes_sub_classes (class_id, sub_class_id) VALUES (:class, :sub_class_id)", {"class": i, "sub_class_id": id})
						classes = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE sub_class_id = :id", {'id': id})
						sub_class[0]['classes'] = classes
						answer = {"data": sub_class, "status": 201}
						return answer, 201
					else:
						answer = {"data": "This id of sub types - "+str(no_id)+" not exist!", "status": 400}
						return answer, 400
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
		
			elif(data['name'] is not None and data['classes_id'] is not None):
				exist_name = self.db.row("SELECT name FROM sub_classes WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE sub_classes SET name = :name WHERE id = :id", {'id': data['id'], 'name': data['name']})
					self.db.query("DELETE FROM classes_sub_classes WHERE sub_class_id = :id", {"id": id})
					clas = Cls()
					error = False
					for i in data['classes_id']:
						class_id = clas.get(i)[0]
						if(class_id['status'] == 404):
							error = True
							no_id = i
							break
					if(error is False):
						sub_class= self.db.row("SELECT * FROM sub_classes WHERE id = :id", {'id': id})
						for i in data['classes_id']:
							self.db.query("INSERT INTO classes_sub_classes (class_id, sub_class_id) VALUES (:class, :sub_class_id)", {"class": i, "sub_class_id": id})
						classes = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE sub_class_id = :id", {'id': id})
						sub_class[0]['classes'] = classes
						answer = {"data": sub_class, "status": 201}
						return answer, 201
					else:
						answer = {"data": "This id of sub type - "+str(no_id)+" not exist!", "status": 400}
						return answer, 400
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
			elif(data['name'] is not None and data['description'] is not None):
				exist_name = self.db.row("SELECT name FROM classes WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE classes SET name = :name, description = :description WHERE id = :id", {'id': data['id'], 'name': data['name'], 'description': data['description']})
					sub_class = self.db.row("SELECT * FROM sub_classes WHERE id = :id", {'id': id})
					classes = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE sub_class_id = :id", {'id': id})
					sub_class[0]['classes'] = classes
					answer = {"data": sub_class, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
			elif(data['classes_id'] is not None and data['description'] is not None):
				self.db.query("UPDATE sub_classes SET description = :description WHERE id = :id", {'id': data['id'], 'description': data['description']})
				self.db.query("DELETE FROM classes_sub_classes WHERE sub_class_id = :id", {"id": id})
				clas = Cls()
				error = False
				for i in data['classes_id']:
					class_id = clas.get(i)[0]
					if(class_id['status'] == 404):
						error = True
						no_id = i
						break
				if(error is False):
					sub_class = self.db.row("SELECT * FROM sub_classes WHERE id = :id", {'id': id})
					for i in data['classes_id']:
						self.db.query("INSERT INTO classes_sub_classes (class_id, sub_class_id) VALUES (:class, :sub_class_id)", {"class": i, "sub_class_id": id})
					classes = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE sub_class_id = :id", {'id': id})
					sub_class[0]['classes'] = classes
					answer = {"data": sub_class, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This id of sub types - "+str(no_id)+" not exist!", "status": 400}
					return answer, 400
			elif(data['classes_id'] is not None):
				self.db.query("DELETE FROM classes_sub_classes WHERE sub_class_id = :id", {"id": id})
				clas = Cls()
				error = False
				for i in data['classes_id']:
					class_id = clas.get(i)[0]
					if(class_id['status'] == 404):
						error = True
						no_id = i
						break
				if(error is False):
					sub_class= self.db.row("SELECT * FROM sub_classes WHERE id = :id", {'id': id})
					for i in data['classes_id']:
						self.db.query("INSERT INTO classes_sub_classes (class_id, sub_class_id) VALUES (:class, :sub_class_id)", {"class": i, "sub_class_id": id})
					classes = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE sub_class_id = :id", {'id': id})
					sub_class[0]['classes'] = classes
					answer = {"data": sub_class, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This id of sub types - "+str(no_id)+" not exist!", "status": 400}
					return answer, 400
			elif(data['name'] is not None):
				exist_name = self.db.row("SELECT name FROM sub_classes WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE sub_classes SET name = :name WHERE id = :id", {'id': data['id'], 'name': data['name']})
					sub_class= self.db.row("SELECT * FROM sub_classes WHERE id = :id", {"id": id})
					classes = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE sub_class_id = :id", {'id': id})
					sub_class[0]['classes'] = classes
					answer = {"data": sub_class, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
			elif(data['description'] is not None):
				self.db.query("UPDATE sub_classes SET description = :description WHERE id = :id", {'id': data['id'], 'description': data['description']})
				sub_class= self.db.row("SELECT * FROM sub_classes WHERE id = :id", {"id": id})
				classes = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE sub_class_id = :id", {'id': id})
				sub_class[0]['classes'] = classes
				answer = {"data": sub_class, "status": 201}
				return answer, 201
		else:
			answer = {"data": "Bad request", 'status': 400}
	def delete(self, id):
		is_id = self.get(id)[0]
		if(is_id['status'] != 404):
			self.db.query("DELETE FROM sub_classes WHERE id = :id; DELETE FROM classes_sub_classes WHERE sub_class_id = :id", {"id": id})
			answer = {"data": "Sub class with id "+str(id)+" is deleted.", 'status': 200}
			return answer, 200
		else:
			answer = {"data": "Bad request", 'status': 400}
			return answer, 400