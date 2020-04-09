from flask_restful import Resource, reqparse
from .familias import Familias
from db import Db

class Genuses(Resource):
	db = Db("encyclopedia", "postgres", "", '127.0.0.1')
	def get(self, id = 0):
		if (id != 0 ): 
			if(len(genuses) > 0):
				genuses = self.db.row("SELECT * FROM genuses WHERE id = :id", {"id": id})
				genuses[0]['familias'] = self.db.row("SELECT familias.id, familias.name FROM familias_genuses RIGHT JOIN familias ON familias_genuses.familia_id = familias.id WHERE genus_id = :id", {'id': id})
				genuses[0]['ordos'] = []
				genuses[0]['sub_classes'] = []
				genuses[0]['classes'] = []
				genuses[0]['sub_types'] = []
				genuses[0]['types'] = []
				genuses[0]['kinds'] = []
				genuses[0]['domains'] = []
				for familia in genuses[0]['familias']:
					ordos = self.db.row("SELECT ordos.id, ordos.name FROM ordos_familias RIGHT JOIN ordos ON ordos_familias.ordo_id = ordos.id WHERE ordos_familias.familia_id = :id GROUP BY ordos.id", {'id': familia['id']})
					for ordo in ordos:
						if ordo not in genuses[0]['ordos']:
							genuses[0]['ordos'].append(ordo)
				for ordo in genuses[0]['ordos']:
					sub_classes = self.db.row("SELECT sub_classes.id, sub_classes.name FROM sub_classes_ordos RIGHT JOIN sub_classes ON sub_classes_ordos.sub_class_id = sub_classes.id WHERE sub_classes_ordos.ordo_id = :id GROUP BY sub_classes.id", {'id': ordo['id']})
					for sub_class in sub_classes:
						if sub_class not in genuses[0]['sub_classes']:
							genuses[0]['sub_classes'].append(sub_class)
				for sub_class in genuses[0]['sub_classes']:
					classes = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE classes_sub_classes.sub_class_id = :id GROUP BY classes.id", {'id': sub_class['id']})
					for clas in classes:
						if clas not in genuses[0]['classes']:
							genuses[0]['classes'].append(clas)
				for clas in genuses[0]['classes']:
					sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE sub_types_classes.class_id = :id GROUP BY sub_types.id", {'id': clas['id']})
					for sub_type in sub_types:
						if sub_type not in genuses[0]['sub_types']:
							genuses[0]['sub_types'].append(sub_type)
				for sub_type in genuses[0]['sub_types']:
					types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE types_sub_types.sub_type_id = :id GROUP BY types.id", {'id': sub_type['id']})
					for type in types:
						if type not in genuses[0]['types']:
							genuses[0]['types'].append(type)
				for type in genuses[0]['types']:
					kinds = self.db.row("SELECT kinds.id, kinds.name FROM types RIGHT JOIN kinds ON types.kind_id = kinds.id WHERE types.id = :id GROUP BY kinds.id", {'id': type['id']})
					for kind in kinds:
						if kind not in genuses[0]['kinds']:
							genuses[0]['kinds'].append(kind)
				for kind in genuses[0]['kinds']:
					domains = self.db.row("SELECT domains.id, domains.name FROM kinds RIGHT JOIN domains ON kinds.domain_id = domains.id WHERE kinds.id = :id GROUP BY domains.id", {'id': kind['id']})
					for domain in domains:
						if domain not in genuses[0]['domains']:
							genuses[0]['domains'].append(domain)	
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
				genuses = self.db.row("SELECT * FROM genuses")
			elif(order == 'ASC'):
				genuses = self.db.row("SELECT * FROM genuses ORDER BY name ASC")
			elif(order == 'DESC'):
				genuses = self.db.row("SELECT * FROM genuses ORDER BY name DESC")
			else:
				genuses = self.db.row("SELECT * FROM genuses")
			for genus in genuses:
				genus['familias'] = self.db.row("SELECT familias.id, familias.name FROM familias_genuses RIGHT JOIN familias ON familias_genuses.familia_id = familias.id WHERE genus_id = :id", {'id': genus['id']})
				genus['ordos'] = []
				genus['sub_classes'] = []
				genus['classes'] = []
				genus['sub_types'] = []
				genus['types'] = []
				genus['kinds'] = []
				genus['domains'] = []
				for familia in genus['familias']:
					ordos = self.db.row("SELECT ordos.id, ordos.name FROM ordos_familias RIGHT JOIN ordos ON ordos_familias.ordo_id = ordos.id WHERE ordos_familias.familia_id = :id GROUP BY ordos.id", {'id': familia['id']})
					for ordo in ordos:
						if ordo not in genus['ordos']:
							genus['ordos'].append(ordo)
				for ordo in genus['ordos']:
					sub_classes = self.db.row("SELECT sub_classes.id, sub_classes.name FROM sub_classes_ordos RIGHT JOIN sub_classes ON sub_classes_ordos.sub_class_id = sub_classes.id WHERE sub_classes_ordos.ordo_id = :id GROUP BY sub_classes.id", {'id': ordo['id']})
					for sub_class in sub_classes:
						if sub_class not in genus['sub_classes']:
							genus['sub_classes'].append(sub_class)
				for sub_class in genus['sub_classes']:
					classes = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE classes_sub_classes.sub_class_id = :id GROUP BY classes.id", {'id': sub_class['id']})
					for clas in classes:
						if clas not in genus['classes']:
							genus['classes'].append(clas)
				for clas in genus['classes']:
					sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE sub_types_classes.class_id = :id GROUP BY sub_types.id", {'id': clas['id']})
					for sub_type in sub_types:
						if sub_type not in genus['sub_types']:
							genus['sub_types'].append(sub_type)
				for sub_type in genus['sub_types']:
					types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE types_sub_types.sub_type_id = :id GROUP BY types.id", {'id': sub_type['id']})
					for type in types:
						if type not in genus['types']:
							genus['types'].append(type)
				for type in genus['types']:
					kinds = self.db.row("SELECT kinds.id, kinds.name FROM types RIGHT JOIN kinds ON types.kind_id = kinds.id WHERE types.id = :id GROUP BY kinds.id", {'id': type['id']})
					for kind in kinds:
						if kind not in genus['kinds']:
							genus['kinds'].append(kind)
				for kind in genus['kinds']:
					domains = self.db.row("SELECT domains.id, domains.name FROM kinds RIGHT JOIN domains ON kinds.domain_id = domains.id WHERE kinds.id = :id GROUP BY domains.id", {'id': kind['id']})
					for domain in domains:
						if domain not in genus['domains']:
							genus['domains'].append(domain)	
			for filter_name, filter_val in filters.items():
				for genus in genuses:
					for s in genus[filter_name]:
						if(filter_val != s['id']):
							genuses.remove(genus)
		if(len(genuses) > 0):
			answer = {"data": genuses, 'status': 200}
			return answer, 200
		else:
			answer = {"data": [], 'status': 404}
			return answer, 404
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
		parser.add_argument('familias_id', type=int, action='append', required=True, help="Type(s) id cannot be blank!")
		parser.add_argument('description', type=str, required=True, help="Description id cannot be blank!")
		data = parser.parse_args()
		exist_name = self.db.row("SELECT name FROM genuses WHERE name = :name", {"name": data['name']})
		if(len(exist_name) == 0):
			familias = Familias()
			error = False
			for i in data['familias_id']:
				familia_id = familias.get(i)[0]
				if(familia_id['status'] == 404):
					error = True
					no_id = i
					break
			if(error is False):
				genus_id = self.db.row("INSERT INTO genuses (name, description) VALUES (:name, :description) RETURNING id", data)
				genus = self.db.row("SELECT * FROM genuses WHERE id = :id", genus_id[0])
				for i in data['familias_id']:
					self.db.query("INSERT INTO familias_genuses (familia_id, genus_id) VALUES (:class, :genus_id)", {"class": i, "genus_id": genus[0]['id']})
				familias = self.db.row("SELECT familias.id, familias.name FROM familias_genuses RIGHT JOIN familias ON familias_genuses.familia_id = familias.id WHERE genus_id = :id", {'id': genus[0]['id']})
				genus[0]['familias'] = familias
				answer = {"data": genus, "status": 201}
				return answer, 201
			else:
				answer = {"data": "This id of familias - "+str(no_id)+" not exist!", "status": 400}
				return answer, 400
		else:
			answer = {"data": "This name already exist!", "status": 400}
			return answer, 400
	def put(self, id):
		parser = reqparse.RequestParser()
		parser.add_argument('name')
		parser.add_argument('familias_id', action='append')
		parser.add_argument('description')
		data = parser.parse_args()
		data['id'] = id
		is_id = self.get(id)[0]
		if(is_id['status'] != 404):
			if(data['name'] is not None and data['familias_id'] is not None and data['description'] is not None):
				exist_name = self.db.row("SELECT name FROM genuses WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE genuses SET name = :name, description = :description WHERE id = :id", {'id': data['id'], 'name': data['name'], 'description': data['description']})
					self.db.query("DELETE FROM familias_genuses WHERE genus_id = :id", {"id": id})
					familia = Familias()
					error = False
					for i in data['familias_id']:
						familia_id = familia.get(i)[0]
						if(familia_id['status'] == 404):
							error = True
							no_id = i
							break
					if(error is False):
						genus = self.db.row("SELECT * FROM genuses WHERE id = :id", {'id': id})
						for i in data['familias_id']:
							self.db.query("INSERT INTO familias_genuses (familia_id, genus_id) VALUES (:class, :genus_id)", {"class": i, "genus_id": id})
						familias = self.db.row("SELECT familias.id, familias.name FROM familias_genuses RIGHT JOIN familias ON familias_genuses.familia_id = familias.id WHERE genus_id = :id", {'id': id})
						genus[0]['familias'] = familias
						answer = {"data": genus, "status": 201}
						return answer, 201
					else:
						answer = {"data": "This id of familias - "+str(no_id)+" not exist!", "status": 400}
						return answer, 400
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
		
			elif(data['name'] is not None and data['familias_id'] is not None):
				exist_name = self.db.row("SELECT name FROM genuses WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE genuses SET name = :name WHERE id = :id", {'id': data['id'], 'name': data['name']})
					self.db.query("DELETE FROM familias_genuses WHERE genus_id = :id", {"id": id})
					familia = Familias()
					error = False
					for i in data['familias_id']:
						familia_id = familia.get(i)[0]
						if(familia_id['status'] == 404):
							error = True
							no_id = i
							break
					if(error is False):
						genus = self.db.row("SELECT * FROM genuses WHERE id = :id", {'id': id})
						for i in data['familias_id']:
							self.db.query("INSERT INTO familias_genuses (familia_id, genus_id) VALUES (:class, :genus_id)", {"class": i, "genus_id": id})
						familias = self.db.row("SELECT familias.id, familias.name FROM familias_genuses RIGHT JOIN familias ON familias_genuses.familia_id = familias.id WHERE genus_id = :id", {'id': id})
						genus[0]['familias'] = familias
						answer = {"data": genus, "status": 201}
						return answer, 201
					else:
						answer = {"data": "This id of familias - "+str(no_id)+" not exist!", "status": 400}
						return answer, 400
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
			elif(data['name'] is not None and data['description'] is not None):
				exist_name = self.db.row("SELECT name FROM familias WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE familias SET name = :name, description = :description WHERE id = :id", {'id': data['id'], 'name': data['name'], 'description': data['description']})
					genus = self.db.row("SELECT * FROM genuses WHERE id = :id", {'id': id})
					familias = self.db.row("SELECT familias.id, familias.name FROM familias_genuses RIGHT JOIN familias ON familias_genuses.familia_id = familias.id WHERE genus_id = :id", {'id': id})
					genus[0]['familias'] = familias
					answer = {"data": genus, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
			elif(data['familias_id'] is not None and data['description'] is not None):
				self.db.query("UPDATE genuses SET description = :description WHERE id = :id", {'id': data['id'], 'description': data['description']})
				self.db.query("DELETE FROM familias_genuses WHERE genus_id = :id", {"id": id})
				familia = Familias()
				error = False
				for i in data['familias_id']:
					familia_id = familia.get(i)[0]
					if(familia_id['status'] == 404):
						error = True
						no_id = i
						break
				if(error is False):
					genus = self.db.row("SELECT * FROM genuses WHERE id = :id", {'id': id})
					for i in data['familias_id']:
						self.db.query("INSERT INTO familias_genuses (familia_id, genus_id) VALUES (:class, :genus_id)", {"class": i, "genus_id": id})
					familias = self.db.row("SELECT familias.id, familias.name FROM familias_genuses RIGHT JOIN familias ON familias_genuses.familia_id = familias.id WHERE genus_id = :id", {'id': id})
					genus[0]['familias'] = familias
					answer = {"data": genus, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This id of familias - "+str(no_id)+" not exist!", "status": 400}
					return answer, 400
			elif(data['familias_id'] is not None):
				self.db.query("DELETE FROM familias_genuses WHERE genus_id = :id", {"id": id})
				familia = Familias()
				error = False
				for i in data['familias_id']:
					familia_id = familia.get(i)[0]
					if(familia_id['status'] == 404):
						error = True
						no_id = i
						break
				if(error is False):
					genus = self.db.row("SELECT * FROM genuses WHERE id = :id", {'id': id})
					for i in data['familias_id']:
						self.db.query("INSERT INTO familias_genuses (familia_id, genus_id) VALUES (:class, :genus_id)", {"class": i, "genus_id": id})
					familias = self.db.row("SELECT familias.id, familias.name FROM familias_genuses RIGHT JOIN familias ON familias_genuses.familia_id = familias.id WHERE genus_id = :id", {'id': id})
					genus[0]['familias'] = familias
					answer = {"data": genus, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This id of familias - "+str(no_id)+" not exist!", "status": 400}
					return answer, 400
			elif(data['name'] is not None):
				exist_name = self.db.row("SELECT name FROM genuses WHERE name = :name", {"name": data['name']})
				if(len(exist_name) == 0):
					self.db.query("UPDATE genuses SET name = :name WHERE id = :id", {'id': data['id'], 'name': data['name']})
					genus = self.db.row("SELECT * FROM genuses WHERE id = :id", {"id": id})
					familias = self.db.row("SELECT familias.id, familias.name FROM familias_genuses RIGHT JOIN familias ON familias_genuses.familia_id = familias.id WHERE genus_id = :id", {'id': id})
					genus[0]['familias'] = familias
					answer = {"data": genus, "status": 201}
					return answer, 201
				else:
					answer = {"data": "This name already exist!", "status": 400}
					return answer, 400
			elif(data['description'] is not None):
				self.db.query("UPDATE genuses SET description = :description WHERE id = :id", {'id': data['id'], 'description': data['description']})
				genus = self.db.row("SELECT * FROM genuses WHERE id = :id", {"id": id})
				familias = self.db.row("SELECT familias.id, familias.name FROM familias_genuses RIGHT JOIN familias ON familias_genuses.familia_id = familias.id WHERE genus_id = :id", {'id': id})
				genus[0]['familias'] = familias
				answer = {"data": genus, "status": 201}
				return answer, 201
		else:
			answer = {"data": "Bad request", 'status': 400}
	def delete(self, id):
		is_id = self.get(id)[0]
		if(is_id['status'] != 404):
			self.db.query("DELETE FROM genuses WHERE id = :id; DELETE FROM familias_genuses WHERE genus_id = :id", {"id": id})
			answer = {"data": "Ordo with id "+str(id)+" is deleted.", 'status': 200}
			return answer, 200
		else:
			answer = {"data": "Bad request", 'status': 400}
			return answer, 400