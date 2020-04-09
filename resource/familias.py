from flask_restful import Resource, reqparse
from .ordos import Ordos
from db import Db

class Familias(Resource):
	db = Db("encyclopedia", "postgres", "", '127.0.0.1')
	def get(self, id = 0):
		if (id != 0 ): 
			if(len(familias) > 0):
				familias = self.db.row("SELECT * FROM familias WHERE id = :id", {"id": id})
				familias[0]['ordos'] = self.db.row("SELECT ordos.id, ordos.name FROM ordos_familias RIGHT JOIN ordos ON ordos_familias.ordo_id = ordos.id WHERE familia_id = :id", {'id': id})
				familias[0]['sub_classes'] = []
				familias[0]['classes'] = []
				familias[0]['sub_types'] = []
				familias[0]['types'] = []
				familias[0]['kinds'] = []
				familias[0]['domains'] = []
				for familia in familias[0]['familias']:
					ordos = self.db.row("SELECT ordos.id, ordos.name FROM ordos_familias RIGHT JOIN ordos ON ordos_familias.ordo_id = ordos.id WHERE ordos_familias.familia_id = :id GROUP BY ordos.id", {'id': familia['id']})
					for ordo in ordos:
						if ordo not in familias[0]['ordos']:
							familias[0]['ordos'].append(ordo)
				for ordo in familias[0]['ordos']:
					sub_classes = self.db.row("SELECT sub_classes.id, sub_classes.name FROM sub_classes_ordos RIGHT JOIN sub_classes ON sub_classes_ordos.sub_class_id = sub_classes.id WHERE sub_classes_ordos.ordo_id = :id GROUP BY sub_classes.id", {'id': ordo['id']})
					for sub_class in sub_classes:
						if sub_class not in familias[0]['sub_classes']:
							familias[0]['sub_classes'].append(sub_class)
				for sub_class in familias[0]['sub_classes']:
					classes = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE classes_sub_classes.sub_class_id = :id GROUP BY classes.id", {'id': sub_class['id']})
					for clas in classes:
						if clas not in familias[0]['classes']:
							familias[0]['classes'].append(clas)
				for clas in familias[0]['classes']:
					sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE sub_types_classes.class_id = :id GROUP BY sub_types.id", {'id': clas['id']})
					for sub_type in sub_types:
						if sub_type not in familias[0]['sub_types']:
							familias[0]['sub_types'].append(sub_type)
				for sub_type in familias[0]['sub_types']:
					types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE types_sub_types.sub_type_id = :id GROUP BY types.id", {'id': sub_type['id']})
					for type in types:
						if type not in familias[0]['types']:
							familias[0]['types'].append(type)
				for type in familias[0]['types']:
					kinds = self.db.row("SELECT kinds.id, kinds.name FROM types RIGHT JOIN kinds ON types.kind_id = kinds.id WHERE types.id = :id GROUP BY kinds.id", {'id': type['id']})
					for kind in kinds:
						if kind not in familias[0]['kinds']:
							familias[0]['kinds'].append(kind)
				for kind in familias[0]['kinds']:
					domains = self.db.row("SELECT domains.id, domains.name FROM kinds RIGHT JOIN domains ON kinds.domain_id = domains.id WHERE kinds.id = :id GROUP BY domains.id", {'id': kind['id']})
					for domain in domains:
						if domain not in familias[0]['domains']:
							familias[0]['domains'].append(domain)	
		else:
			parser = reqparse.RequestParser()
			ordparser = reqparse.RequestParser()
			parser.add_argument('domains', type=int)
			parser.add_argument('kinds', type=int)
			parser.add_argument('types', type=int)
			parser.add_argument('sub_types', type=int)
			parser.add_argument('classes', type=int)
			parser.add_argument('sub_classes', type=int)
			parser.add_argument('ordos', type=int)
			parser.add_argument('familias', type=int)
			data = parser.parse_args()
			ordparser.add_argument('order', type=str)
			order = ordparser.parse_args()['order']
			filters = dict(filter(lambda elem: elem[1] is not None, data.items()))
			if(order is None):
				familias = self.db.row("SELECT * FROM familias")
			elif(order == 'ASC'):
				familias = self.db.row("SELECT * FROM familias ORDER BY name ASC")
			elif(order == 'DESC'):
				familias = self.db.row("SELECT * FROM familias ORDER BY name DESC")
			else:
				familias = self.db.row("SELECT * FROM familias")
			for familia in familias:
				familia['ordos'] = self.db.row("SELECT ordos.id, ordos.name FROM ordos_familias RIGHT JOIN ordos ON ordos_familias.ordo_id = ordos.id WHERE familia_id = :id", {'id': familia['id']})
				familia['sub_classes'] = []
				familia['classes'] = []
				familia['sub_types'] = []
				familia['types'] = []
				familia['kinds'] = []
				familia['domains'] = []
				for familia in familia['familias']:
					ordos = self.db.row("SELECT ordos.id, ordos.name FROM ordos_familias RIGHT JOIN ordos ON ordos_familias.ordo_id = ordos.id WHERE ordos_familias.familia_id = :id GROUP BY ordos.id", {'id': familia['id']})
					for ordo in ordos:
						if ordo not in familia['ordos']:
							familia['ordos'].append(ordo)
				for ordo in familia['ordos']:
					sub_classes = self.db.row("SELECT sub_classes.id, sub_classes.name FROM sub_classes_ordos RIGHT JOIN sub_classes ON sub_classes_ordos.sub_class_id = sub_classes.id WHERE sub_classes_ordos.ordo_id = :id GROUP BY sub_classes.id", {'id': ordo['id']})
					for sub_class in sub_classes:
						if sub_class not in familia['sub_classes']:
							familia['sub_classes'].append(sub_class)
				for sub_class in familia['sub_classes']:
					classes = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE classes_sub_classes.sub_class_id = :id GROUP BY classes.id", {'id': sub_class['id']})
					for clas in classes:
						if clas not in familia['classes']:
							familia['classes'].append(clas)
				for clas in familia['classes']:
					sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE sub_types_classes.class_id = :id GROUP BY sub_types.id", {'id': clas['id']})
					for sub_type in sub_types:
						if sub_type not in familia['sub_types']:
							familia['sub_types'].append(sub_type)
				for sub_type in familia['sub_types']:
					types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE types_sub_types.sub_type_id = :id GROUP BY types.id", {'id': sub_type['id']})
					for type in types:
						if type not in familia['types']:
							familia['types'].append(type)
				for type in familia['types']:
					kinds = self.db.row("SELECT kinds.id, kinds.name FROM types RIGHT JOIN kinds ON types.kind_id = kinds.id WHERE types.id = :id GROUP BY kinds.id", {'id': type['id']})
					for kind in kinds:
						if kind not in familia['kinds']:
							familia['kinds'].append(kind)
				for kind in familia['kinds']:
					domains = self.db.row("SELECT domains.id, domains.name FROM kinds RIGHT JOIN domains ON kinds.domain_id = domains.id WHERE kinds.id = :id GROUP BY domains.id", {'id': kind['id']})
					for domain in domains:
						if domain not in familia['domains']:
							familia['domains'].append(domain)	
			for filter_name, filter_val in filters.items():
				for familia in familias:
					for s in familia[filter_name]:
						if(filter_val != s['id']):
							familias.remove(familia)

		if(len(familias) > 0):
			answer = {"data": familias, 'status': 200}
			return answer, 200
		else:
			answer = {"data": [], 'status': 404}
			return answer, 404
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
		parser.add_argument('ordos_id', type=int, action='append', required=True, help="Type(s) id cannot be blank!")
		parser.add_argument('description', type=str, required=True, help="Description id cannot be blank!")
		data = parser.parse_args()
		exist_name = self.db.row("SELECT name FROM familias WHERE name = :name", {"name": data['name']})
		if(len(exist_name) == 0):
			ordos = Ordos()
			error = False
			for i in data['ordos_id']:
				ordo_id = ordos.get(i)[0]
				if(ordo_id['status'] == 404):
					error = True
					no_id = i
					break
			if(error is False):
				familia_id = self.db.row("INSERT INTO familias (name, description) VALUES (:name, :description) RETURNING id", data)
				familia = self.db.row("SELECT * FROM familias WHERE id = :id", familia_id[0])
				for i in data['ordos_id']:
					self.db.query("INSERT INTO ordos_familias (ordo_id, familia_id) VALUES (:class, :familia_id)", {"class": i, "familia_id": familia[0]['id']})
				ordos = self.db.row("SELECT ordos.id, ordos.name FROM ordos_familias RIGHT JOIN ordos ON ordos_familias.ordo_id = ordos.id WHERE familia_id = :id", {'id': familia[0]['id']})
				familia[0]['ordos'] = ordos
				answer = {"data": familia, "status": 201}
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
		parser.add_argument('ordos_id', action='append')
		parser.add_argument('description')
		data = parser.parse_args()
		data['id'] = id
		is_id = self.get(id)[0]
		if(is_id['status'] != 404):
			if(data['name'] is not None and data['ordos_id'] is not None and data['description'] is not None):
				exist_name = self.db.row("SELECT name FROM familias WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE familias SET name = :name, description = :description WHERE id = :id", {'id': data['id'], 'name': data['name'], 'description': data['description']})
					self.db.query("DELETE FROM ordos_familias WHERE familia_id = :id", {"id": id})
					ordo = Ordos()
					error = False
					for i in data['ordos_id']:
						ordo_id = ordo.get(i)[0]
						if(ordo_id['status'] == 404):
							error = True
							no_id = i
							break
					if(error is False):
						familia = self.db.row("SELECT * FROM familias WHERE id = :id", {'id': id})
						for i in data['ordos_id']:
							self.db.query("INSERT INTO ordos_familias (ordo_id, familia_id) VALUES (:class, :familia_id)", {"class": i, "familia_id": id})
						ordos = self.db.row("SELECT ordos.id, ordos.name FROM ordos_familias RIGHT JOIN ordos ON ordos_familias.ordo_id = ordos.id WHERE familia_id = :id", {'id': id})
						familia[0]['ordos'] = ordos
						answer = {"data": familia, "status": 201}
						return answer, 201
					else:
						answer = {"data": "This id of sub types - "+str(no_id)+" not exist!", "status": 400}
						return answer, 400
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
		
			elif(data['name'] is not None and data['ordos_id'] is not None):
				exist_name = self.db.row("SELECT name FROM familias WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE familias SET name = :name WHERE id = :id", {'id': data['id'], 'name': data['name']})
					self.db.query("DELETE FROM ordos_familias WHERE familia_id = :id", {"id": id})
					ordo = Ordos()
					error = False
					for i in data['ordos_id']:
						ordo_id = ordo.get(i)[0]
						if(ordo_id['status'] == 404):
							error = True
							no_id = i
							break
					if(error is False):
						familia = self.db.row("SELECT * FROM familias WHERE id = :id", {'id': id})
						for i in data['ordos_id']:
							self.db.query("INSERT INTO ordos_familias (ordo_id, familia_id) VALUES (:class, :familia_id)", {"class": i, "familia_id": id})
						ordos = self.db.row("SELECT ordos.id, ordos.name FROM ordos_familias RIGHT JOIN ordos ON ordos_familias.ordo_id = ordos.id WHERE familia_id = :id", {'id': id})
						familia[0]['ordos'] = ordos
						answer = {"data": familia, "status": 201}
						return answer, 201
					else:
						answer = {"data": "This id of sub type - "+str(no_id)+" not exist!", "status": 400}
						return answer, 400
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
			elif(data['name'] is not None and data['description'] is not None):
				exist_name = self.db.row("SELECT name FROM ordos WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE ordos SET name = :name, description = :description WHERE id = :id", {'id': data['id'], 'name': data['name'], 'description': data['description']})
					familia = self.db.row("SELECT * FROM familias WHERE id = :id", {'id': id})
					ordos = self.db.row("SELECT ordos.id, ordos.name FROM ordos_familias RIGHT JOIN ordos ON ordos_familias.ordo_id = ordos.id WHERE familia_id = :id", {'id': id})
					familia[0]['ordos'] = ordos
					answer = {"data": familia, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
			elif(data['ordos_id'] is not None and data['description'] is not None):
				self.db.query("UPDATE familias SET description = :description WHERE id = :id", {'id': data['id'], 'description': data['description']})
				self.db.query("DELETE FROM ordos_familias WHERE familia_id = :id", {"id": id})
				ordo = Ordos()
				error = False
				for i in data['ordos_id']:
					ordo_id = ordo.get(i)[0]
					if(ordo_id['status'] == 404):
						error = True
						no_id = i
						break
				if(error is False):
					familia = self.db.row("SELECT * FROM familias WHERE id = :id", {'id': id})
					for i in data['ordos_id']:
						self.db.query("INSERT INTO ordos_familias (ordo_id, familia_id) VALUES (:class, :familia_id)", {"class": i, "familia_id": id})
					ordos = self.db.row("SELECT ordos.id, ordos.name FROM ordos_familias RIGHT JOIN ordos ON ordos_familias.ordo_id = ordos.id WHERE familia_id = :id", {'id': id})
					familia[0]['ordos'] = ordos
					answer = {"data": familia, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This id of sub types - "+str(no_id)+" not exist!", "status": 400}
					return answer, 400
			elif(data['ordos_id'] is not None):
				self.db.query("DELETE FROM ordos_familias WHERE familia_id = :id", {"id": id})
				ordo = Ordos()
				error = False
				for i in data['ordos_id']:
					ordo_id = ordo.get(i)[0]
					if(ordo_id['status'] == 404):
						error = True
						no_id = i
						break
				if(error is False):
					familia = self.db.row("SELECT * FROM familias WHERE id = :id", {'id': id})
					for i in data['ordos_id']:
						self.db.query("INSERT INTO ordos_familias (ordo_id, familia_id) VALUES (:class, :familia_id)", {"class": i, "familia_id": id})
					ordos = self.db.row("SELECT ordos.id, ordos.name FROM ordos_familias RIGHT JOIN ordos ON ordos_familias.ordo_id = ordos.id WHERE familia_id = :id", {'id': id})
					familia[0]['ordos'] = ordos
					answer = {"data": familia, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This id of sub types - "+str(no_id)+" not exist!", "status": 400}
					return answer, 400
			elif(data['name'] is not None):
				exist_name = self.db.row("SELECT name FROM familias WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE familias SET name = :name WHERE id = :id", {'id': data['id'], 'name': data['name']})
					familia = self.db.row("SELECT * FROM familias WHERE id = :id", {"id": id})
					ordos = self.db.row("SELECT ordos.id, ordos.name FROM ordos_familias RIGHT JOIN ordos ON ordos_familias.ordo_id = ordos.id WHERE familia_id = :id", {'id': id})
					familia[0]['ordos'] = ordos
					answer = {"data": familia, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
			elif(data['description'] is not None):
				self.db.query("UPDATE familias SET description = :description WHERE id = :id", {'id': data['id'], 'description': data['description']})
				familia = self.db.row("SELECT * FROM familias WHERE id = :id", {"id": id})
				ordos = self.db.row("SELECT ordos.id, ordos.name FROM ordos_familias RIGHT JOIN ordos ON ordos_familias.ordo_id = ordos.id WHERE familia_id = :id", {'id': id})
				familia[0]['ordos'] = ordos
				answer = {"data": familia, "status": 201}
				return answer, 201
		else:
			answer = {"data": "Bad request", 'status': 400}
	def delete(self, id):
		is_id = self.get(id)[0]
		if(is_id['status'] != 404):
			self.db.query("DELETE FROM familias WHERE id = :id; DELETE FROM ordos_familias WHERE familia_id = :id", {"id": id})
			answer = {"data": "Ordo with id "+str(id)+" is deleted.", 'status': 200}
			return answer, 200
		else:
			answer = {"data": "Bad request", 'status': 400}
			return answer, 400