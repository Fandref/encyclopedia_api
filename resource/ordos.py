from flask_restful import Resource, reqparse
from .sub_classes import SubClasses
from db import Db

class Ordos(Resource):
	db = Db("encyclopedia", "postgres", "", '127.0.0.1')
	def get(self, id = 0):
		if (id != 0 ): 
			if(len(ordos) > 0):
				ordos = self.db.row("SELECT * FROM ordos WHERE id = :id", {"id": id})
				ordos[0]['sub_classes'] = self.db.row("SELECT sub_classes.id, sub_classes.name FROM sub_classes_ordos RIGHT JOIN sub_classes ON sub_classes_ordos.sub_class_id = sub_classes.id WHERE ordo_id = :id", {'id': id})
				ordos[0]['classes'] = []
				ordos[0]['sub_types'] = []
				ordos[0]['types'] = []
				ordos[0]['kinds'] = []
				ordos[0]['domains'] = []
				for sub_class in ordos[0]['sub_classes']:
					classes = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE classes_sub_classes.sub_class_id = :id GROUP BY classes.id", {'id': sub_class['id']})
					for clas in classes:
						if clas not in ordos[0]['classes']:
							ordos[0]['classes'].append(clas)
				for clas in ordos[0]['classes']:
					sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE sub_types_classes.class_id = :id GROUP BY sub_types.id", {'id': clas['id']})
					for sub_type in sub_types:
						if sub_type not in ordos[0]['sub_types']:
							ordos[0]['sub_types'].append(sub_type)
				for sub_type in ordos[0]['sub_types']:
					types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE types_sub_types.sub_type_id = :id GROUP BY types.id", {'id': sub_type['id']})
					for type in types:
						if type not in ordos[0]['types']:
							ordos[0]['types'].append(type)
				for type in ordos[0]['types']:
					kinds = self.db.row("SELECT kinds.id, kinds.name FROM types RIGHT JOIN kinds ON types.kind_id = kinds.id WHERE types.id = :id GROUP BY kinds.id", {'id': type['id']})
					for kind in kinds:
						if kind not in ordos[0]['kinds']:
							ordos[0]['kinds'].append(kind)
				for kind in ordos[0]['kinds']:
					domains = self.db.row("SELECT domains.id, domains.name FROM kinds RIGHT JOIN domains ON kinds.domain_id = domains.id WHERE kinds.id = :id GROUP BY domains.id", {'id': kind['id']})
					for domain in domains:
						if domain not in ordos[0]['domains']:
							ordos[0]['domains'].append(domain)	
		else:
			parser = reqparse.RequestParser()
			ordparser = reqparse.RequestParser()
			parser.add_argument('domains', type=int)
			parser.add_argument('kinds', type=int)
			parser.add_argument('types', type=int)
			parser.add_argument('sub_types', type=int)
			parser.add_argument('classes', type=int)
			parser.add_argument('sub_classes', type=int)
			data = parser.parse_args()
			ordparser.add_argument('order', type=str)
			order = ordparser.parse_args()['order']
			filters = dict(filter(lambda elem: elem[1] is not None, data.items()))
			if(order is None):
				ordos = self.db.row("SELECT * FROM ordos")
			elif(order == 'ASC'):
				ordos = self.db.row("SELECT * FROM ordos ORDER BY name ASC")
			elif(order == 'DESC'):
				ordos = self.db.row("SELECT * FROM ordos ORDER BY name DESC")
			else:
				ordos = self.db.row("SELECT * FROM ordos")
			for ordo in ordos:
				ordo['sub_classes'] = self.db.row("SELECT sub_classes.id, sub_classes.name FROM sub_classes_ordos RIGHT JOIN sub_classes ON sub_classes_ordos.sub_class_id = sub_classes.id WHERE ordo_id = :id", {'id': ordo['id']})
				ordo['classes'] = []
				ordo['sub_types'] = []
				ordo['types'] = []
				ordo['kinds'] = []
				ordo['domains'] = []
				for sub_class in ordo['sub_classes']:
					classes = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE classes_sub_classes.sub_class_id = :id GROUP BY classes.id", {'id': sub_class['id']})
					for clas in classes:
						if clas not in ordo['classes']:
							ordo['classes'].append(clas)
				for clas in ordo['classes']:
					sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE sub_types_classes.class_id = :id GROUP BY sub_types.id", {'id': clas['id']})
					for sub_type in sub_types:
						if sub_type not in ordo['sub_types']:
							ordo['sub_types'].append(sub_type)
				for sub_type in ordo['sub_types']:
					types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE types_sub_types.sub_type_id = :id GROUP BY types.id", {'id': sub_type['id']})
					for type in types:
						if type not in ordo['types']:
							ordo['types'].append(type)
				for type in ordo['types']:
					kinds = self.db.row("SELECT kinds.id, kinds.name FROM types RIGHT JOIN kinds ON types.kind_id = kinds.id WHERE types.id = :id GROUP BY kinds.id", {'id': type['id']})
					for kind in kinds:
						if kind not in ordo['kinds']:
							ordo['kinds'].append(kind)
				for kind in ordo['kinds']:
					domains = self.db.row("SELECT domains.id, domains.name FROM kinds RIGHT JOIN domains ON kinds.domain_id = domains.id WHERE kinds.id = :id GROUP BY domains.id", {'id': kind['id']})
					for domain in domains:
						if domain not in ordo['domains']:
							ordo['domains'].append(domain)	
			for filter_name, filter_val in filters.items():
				for ordo in ordos:
					for s in ordo[filter_name]:
						if(filter_val != s['id']):
							ordos.remove(ordo)
		if(len(ordos) > 0):
			answer = {"data": ordos, 'status': 200}
			return answer, 200
		else:
			answer = {"data": [], 'status': 404}
			return answer, 404

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
		parser.add_argument('sub_classes_id', type=int, action='append', required=True, help="Type(s) id cannot be blank!")
		parser.add_argument('description', type=str, required=True, help="Description id cannot be blank!")
		data = parser.parse_args()
		exist_name = self.db.row("SELECT name FROM ordos WHERE name = :name", {"name": data['name']})
		if(len(exist_name) == 0):
			sub_classes = SubClasses()
			error = False
			for i in data['sub_classes_id']:
				sub_class_id = sub_classes.get(i)[0]
				if(sub_class_id['status'] == 404):
					error = True
					no_id = i
					break
			if(error is False):
				ordo_id = self.db.row("INSERT INTO ordos (name, description) VALUES (:name, :description) RETURNING id", data)
				ordo= self.db.row("SELECT * FROM ordos WHERE id = :id", ordo_id[0])
				for i in data['sub_classes_id']:
					self.db.query("INSERT INTO sub_classes_ordos (sub_class_id, ordo_id) VALUES (:class, :ordo_id)", {"class": i, "ordo_id": ordo[0]['id']})
				sub_classes = self.db.row("SELECT sub_classes.id, sub_classes.name FROM sub_classes_ordos RIGHT JOIN sub_classes ON sub_classes_ordos.sub_class_id = sub_classes.id WHERE ordo_id = :id", {'id': ordo[0]['id']})
				ordo[0]['sub_classes'] = sub_classes
				answer = {"data": ordo, "status": 201}
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
		parser.add_argument('sub_classes_id', action='append')
		parser.add_argument('description')
		data = parser.parse_args()
		data['id'] = id
		is_id = self.get(id)[0]
		if(is_id['status'] != 404):
			if(data['name'] is not None and data['sub_classes_id'] is not None and data['description'] is not None):
				exist_name = self.db.row("SELECT name FROM ordos WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE ordos SET name = :name, description = :description WHERE id = :id", {'id': data['id'], 'name': data['name'], 'description': data['description']})
					self.db.query("DELETE FROM sub_classes_ordos WHERE ordo_id = :id", {"id": id})
					sub_class= SubClasses()
					error = False
					for i in data['sub_classes_id']:
						sub_class_id = sub_class.get(i)[0]
						if(sub_class_id['status'] == 404):
							error = True
							no_id = i
							break
					if(error is False):
						ordo= self.db.row("SELECT * FROM ordos WHERE id = :id", {'id': id})
						for i in data['sub_classes_id']:
							self.db.query("INSERT INTO sub_classes_ordos (sub_class_id, ordo_id) VALUES (:class, :ordo_id)", {"class": i, "ordo_id": id})
						sub_classes = self.db.row("SELECT sub_classes.id, sub_classes.name FROM sub_classes_ordos RIGHT JOIN sub_classes ON sub_classes_ordos.sub_class_id = sub_classes.id WHERE ordo_id = :id", {'id': id})
						ordo[0]['sub_classes'] = sub_classes
						answer = {"data": ordo, "status": 201}
						return answer, 201
					else:
						answer = {"data": "This id of sub types - "+str(no_id)+" not exist!", "status": 400}
						return answer, 400
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
		
			elif(data['name'] is not None and data['sub_classes_id'] is not None):
				exist_name = self.db.row("SELECT name FROM ordos WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE ordos SET name = :name WHERE id = :id", {'id': data['id'], 'name': data['name']})
					self.db.query("DELETE FROM sub_classes_ordos WHERE ordo_id = :id", {"id": id})
					sub_class= SubClasses()
					error = False
					for i in data['sub_classes_id']:
						sub_class_id = sub_class.get(i)[0]
						if(sub_class_id['status'] == 404):
							error = True
							no_id = i
							break
					if(error is False):
						ordo= self.db.row("SELECT * FROM ordos WHERE id = :id", {'id': id})
						for i in data['sub_classes_id']:
							self.db.query("INSERT INTO sub_classes_ordos (sub_class_id, ordo_id) VALUES (:class, :ordo_id)", {"class": i, "ordo_id": id})
						sub_classes = self.db.row("SELECT sub_classes.id, sub_classes.name FROM sub_classes_ordos RIGHT JOIN sub_classes ON sub_classes_ordos.sub_class_id = sub_classes.id WHERE ordo_id = :id", {'id': id})
						ordo[0]['sub_classes'] = sub_classes
						answer = {"data": ordo, "status": 201}
						return answer, 201
					else:
						answer = {"data": "This id of sub type - "+str(no_id)+" not exist!", "status": 400}
						return answer, 400
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
			elif(data['name'] is not None and data['description'] is not None):
				exist_name = self.db.row("SELECT name FROM sub_classes WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE sub_classes SET name = :name, description = :description WHERE id = :id", {'id': data['id'], 'name': data['name'], 'description': data['description']})
					ordo = self.db.row("SELECT * FROM ordos WHERE id = :id", {'id': id})
					sub_classes = self.db.row("SELECT sub_classes.id, sub_classes.name FROM sub_classes_ordos RIGHT JOIN sub_classes ON sub_classes_ordos.sub_class_id = sub_classes.id WHERE ordo_id = :id", {'id': id})
					ordo[0]['sub_classes'] = sub_classes
					answer = {"data": ordo, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
			elif(data['sub_classes_id'] is not None and data['description'] is not None):
				self.db.query("UPDATE ordos SET description = :description WHERE id = :id", {'id': data['id'], 'description': data['description']})
				self.db.query("DELETE FROM sub_classes_ordos WHERE ordo_id = :id", {"id": id})
				sub_class= SubClasses()
				error = False
				for i in data['sub_classes_id']:
					sub_class_id = sub_class.get(i)[0]
					if(sub_class_id['status'] == 404):
						error = True
						no_id = i
						break
				if(error is False):
					ordo = self.db.row("SELECT * FROM ordos WHERE id = :id", {'id': id})
					for i in data['sub_classes_id']:
						self.db.query("INSERT INTO sub_classes_ordos (sub_class_id, ordo_id) VALUES (:class, :ordo_id)", {"class": i, "ordo_id": id})
					sub_classes = self.db.row("SELECT sub_classes.id, sub_classes.name FROM sub_classes_ordos RIGHT JOIN sub_classes ON sub_classes_ordos.sub_class_id = sub_classes.id WHERE ordo_id = :id", {'id': id})
					ordo[0]['sub_classes'] = sub_classes
					answer = {"data": ordo, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This id of sub types - "+str(no_id)+" not exist!", "status": 400}
					return answer, 400
			elif(data['sub_classes_id'] is not None):
				self.db.query("DELETE FROM sub_classes_ordos WHERE ordo_id = :id", {"id": id})
				sub_class= SubClasses()
				error = False
				for i in data['sub_classes_id']:
					sub_class_id = sub_class.get(i)[0]
					if(sub_class_id['status'] == 404):
						error = True
						no_id = i
						break
				if(error is False):
					ordo= self.db.row("SELECT * FROM ordos WHERE id = :id", {'id': id})
					for i in data['sub_classes_id']:
						self.db.query("INSERT INTO sub_classes_ordos (sub_class_id, ordo_id) VALUES (:class, :ordo_id)", {"class": i, "ordo_id": id})
					sub_classes = self.db.row("SELECT sub_classes.id, sub_classes.name FROM sub_classes_ordos RIGHT JOIN sub_classes ON sub_classes_ordos.sub_class_id = sub_classes.id WHERE ordo_id = :id", {'id': id})
					ordo[0]['sub_classes'] = sub_classes
					answer = {"data": ordo, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This id of sub types - "+str(no_id)+" not exist!", "status": 400}
					return answer, 400
			elif(data['name'] is not None):
				exist_name = self.db.row("SELECT name FROM ordos WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE ordos SET name = :name WHERE id = :id", {'id': data['id'], 'name': data['name']})
					ordo= self.db.row("SELECT * FROM ordos WHERE id = :id", {"id": id})
					sub_classes = self.db.row("SELECT sub_classes.id, sub_classes.name FROM sub_classes_ordos RIGHT JOIN sub_classes ON sub_classes_ordos.sub_class_id = sub_classes.id WHERE ordo_id = :id", {'id': id})
					ordo[0]['sub_classes'] = sub_classes
					answer = {"data": ordo, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
			elif(data['description'] is not None):
				self.db.query("UPDATE ordos SET description = :description WHERE id = :id", {'id': data['id'], 'description': data['description']})
				ordo= self.db.row("SELECT * FROM ordos WHERE id = :id", {"id": id})
				sub_classes = self.db.row("SELECT sub_classes.id, sub_classes.name FROM sub_classes_ordos RIGHT JOIN sub_classes ON sub_classes_ordos.sub_class_id = sub_classes.id WHERE ordo_id = :id", {'id': id})
				ordo[0]['sub_classes'] = sub_classes
				answer = {"data": ordo, "status": 201}
				return answer, 201
		else:
			answer = {"data": "Bad request", 'status': 400}
	def delete(self, id):
		is_id = self.get(id)[0]
		if(is_id['status'] != 404):
			self.db.query("DELETE FROM ordos WHERE id = :id; DELETE FROM sub_classes_ordos WHERE ordo_id = :id", {"id": id})
			answer = {"data": "Ordo with id "+str(id)+" is deleted.", 'status': 200}
			return answer, 200
		else:
			answer = {"data": "Bad request", 'status': 400}
			return answer, 400