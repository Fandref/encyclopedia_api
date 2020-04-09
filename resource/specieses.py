from flask_restful import Resource, reqparse
from .genuses import Genuses
from .countries import Countries
from db import Db


class Specieses(Resource):
	db = Db("encyclopedia", "postgres", "", '127.0.0.1')
	def get(self, id=0):
		if (id != 0 ): 
			speciese = self.db.row("SELECT image, name, description FROM specieses WHERE id = :id", {"id": id})
			if(len(speciese) > 0):
				speciese[0]['genuses'] = self.db.row("SELECT genuses.id, genuses.name FROM genuses_specieses RIGHT JOIN genuses ON genuses_specieses.genus_id = genuses.id WHERE species_id = :id", {'id': id})
				speciese[0]['familias'] = []
				speciese[0]['ordos'] = []
				speciese[0]['sub_classes'] = []
				speciese[0]['classes'] = []
				speciese[0]['sub_types'] = []
				speciese[0]['types'] = []
				speciese[0]['kinds'] = []
				speciese[0]['domains'] = []
				speciese[0]['countries'] = self.db.row("SELECT countries.id, countries.name FROM countries_specieses RIGHT JOIN countries ON countries_specieses.country_id = countries.id WHERE species_id = :id", {'id': id})
				for genus in speciese[0]['genuses']:
					familias = self.db.row("SELECT familias.id, familias.name FROM familias_genuses RIGHT JOIN familias ON familias_genuses.familia_id = familias.id WHERE familias_genuses.genus_id = :id GROUP BY familias.id", {'id': genus['id']})
					for familia in familias:
						if familia not in speciese[0]['familias']:
							speciese[0]['familias'].append(familia)
				for familia in speciese[0]['familias']:
					ordos = self.db.row("SELECT ordos.id, ordos.name FROM ordos_familias RIGHT JOIN ordos ON ordos_familias.ordo_id = ordos.id WHERE ordos_familias.familia_id = :id GROUP BY ordos.id", {'id': familia['id']})
					for ordo in ordos:
						if ordo not in speciese[0]['ordos']:
							speciese[0]['ordos'].append(ordo)
				for ordo in speciese[0]['ordos']:
					sub_classes = self.db.row("SELECT sub_classes.id, sub_classes.name FROM sub_classes_ordos RIGHT JOIN sub_classes ON sub_classes_ordos.sub_class_id = sub_classes.id WHERE sub_classes_ordos.ordo_id = :id GROUP BY sub_classes.id", {'id': ordo['id']})
					for sub_class in sub_classes:
						if sub_class not in speciese[0]['sub_classes']:
							speciese[0]['sub_classes'].append(sub_class)
				for sub_class in speciese[0]['sub_classes']:
					classes = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE classes_sub_classes.sub_class_id = :id GROUP BY classes.id", {'id': sub_class['id']})
					for clas in classes:
						if clas not in speciese[0]['classes']:
							speciese[0]['classes'].append(clas)
				for clas in speciese[0]['classes']:
					sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE sub_types_classes.class_id = :id GROUP BY sub_types.id", {'id': clas['id']})
					for sub_type in sub_types:
						if sub_type not in speciese[0]['sub_types']:
							speciese[0]['sub_types'].append(sub_type)
				for sub_type in speciese[0]['sub_types']:
					types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE types_sub_types.sub_type_id = :id GROUP BY types.id", {'id': sub_type['id']})
					for type in types:
						if type not in speciese[0]['types']:
							speciese[0]['types'].append(type)
				for type in speciese[0]['types']:
					kinds = self.db.row("SELECT kinds.id, kinds.name FROM types RIGHT JOIN kinds ON types.kind_id = kinds.id WHERE types.id = :id GROUP BY kinds.id", {'id': type['id']})
					for kind in kinds:
						if kind not in speciese[0]['kinds']:
							speciese[0]['kinds'].append(kind)
				for kind in speciese[0]['kinds']:
					domains = self.db.row("SELECT domains.id, domains.name FROM kinds RIGHT JOIN domains ON kinds.domain_id = domains.id WHERE kinds.id = :id GROUP BY domains.id", {'id': kind['id']})
					for domain in domains:
						if domain not in speciese[0]['domains']:
							speciese[0]['domains'].append(domain)	
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
			parser.add_argument('genuses', type=int)
			parser.add_argument('countries', type=int)
			data = parser.parse_args()
			ordparser.add_argument('order', type=str)
			order = ordparser.parse_args()['order']
			filters = dict(filter(lambda elem: elem[1] is not None, data.items()))
			if(order is None):
				speciese = self.db.row("SELECT * FROM specieses")
			elif(order == 'ASC'):
				speciese = self.db.row("SELECT * FROM specieses ORDER BY name ASC")
			elif(order == 'DESC'):
				speciese = self.db.row("SELECT * FROM specieses ORDER BY name DESC")
			else:
				speciese = self.db.row("SELECT * FROM specieses")
			for species in speciese:
				species['genuses'] = self.db.row("SELECT genuses.id, genuses.name FROM genuses_specieses RIGHT JOIN genuses ON genuses_specieses.genus_id = genuses.id WHERE species_id = :id", {'id': species['id']})
				species['familias'] = []
				species['ordos'] = []
				species['sub_classes'] = []
				species['classes'] = []
				species['sub_types'] = []
				species['types'] = []
				species['kinds'] = []
				species['domains'] = []
				species['countries'] = self.db.row("SELECT countries.id, countries.name FROM countries_specieses RIGHT JOIN countries ON countries_specieses.country_id = countries.id WHERE species_id = :id", {'id': species['id']})
				for genus in species['genuses']:
					familias = self.db.row("SELECT familias.id, familias.name FROM familias_genuses RIGHT JOIN familias ON familias_genuses.familia_id = familias.id WHERE familias_genuses.genus_id = :id GROUP BY familias.id", {'id': genus['id']})
					for familia in familias:
						if familia not in species['familias']:
							species['familias'].append(familia)
				for familia in species['familias']:
					ordos = self.db.row("SELECT ordos.id, ordos.name FROM ordos_familias RIGHT JOIN ordos ON ordos_familias.ordo_id = ordos.id WHERE ordos_familias.familia_id = :id GROUP BY ordos.id", {'id': familia['id']})
					for ordo in ordos:
						if ordo not in species['ordos']:
							species['ordos'].append(ordo)
				for ordo in species['ordos']:
					sub_classes = self.db.row("SELECT sub_classes.id, sub_classes.name FROM sub_classes_ordos RIGHT JOIN sub_classes ON sub_classes_ordos.sub_class_id = sub_classes.id WHERE sub_classes_ordos.ordo_id = :id GROUP BY sub_classes.id", {'id': ordo['id']})
					for sub_class in sub_classes:
						if sub_class not in species['sub_classes']:
							species['sub_classes'].append(sub_class)
				for sub_class in species['sub_classes']:
					classes = self.db.row("SELECT classes.id, classes.name FROM classes_sub_classes RIGHT JOIN classes ON classes_sub_classes.class_id = classes.id WHERE classes_sub_classes.sub_class_id = :id GROUP BY classes.id", {'id': sub_class['id']})
					for clas in classes:
						if clas not in species['classes']:
							species['classes'].append(clas)
				for clas in species['classes']:
					sub_types = self.db.row("SELECT sub_types.id, sub_types.name FROM sub_types_classes RIGHT JOIN sub_types ON sub_types_classes.sub_type_id = sub_types.id WHERE sub_types_classes.class_id = :id GROUP BY sub_types.id", {'id': clas['id']})
					for sub_type in sub_types:
						if sub_type not in species['sub_types']:
							species['sub_types'].append(sub_type)
				for sub_type in species['sub_types']:
					types = self.db.row("SELECT types.id, types.name FROM types_sub_types RIGHT JOIN types ON types_sub_types.type_id = types.id WHERE types_sub_types.sub_type_id = :id GROUP BY types.id", {'id': sub_type['id']})
					for type in types:
						if type not in species['types']:
							species['types'].append(type)
				for type in species['types']:
					kinds = self.db.row("SELECT kinds.id, kinds.name FROM types RIGHT JOIN kinds ON types.kind_id = kinds.id WHERE types.id = :id GROUP BY kinds.id", {'id': type['id']})
					for kind in kinds:
						if kind not in species['kinds']:
							species['kinds'].append(kind)
				for kind in species['kinds']:
					domains = self.db.row("SELECT domains.id, domains.name FROM kinds RIGHT JOIN domains ON kinds.domain_id = domains.id WHERE kinds.id = :id GROUP BY domains.id", {'id': kind['id']})
					for domain in domains:
						if domain not in species['domains']:
							species['domains'].append(domain)	
			for filter_name, filter_val in filters.items():
				for species in speciese:
					for s in species[filter_name]:
						if(filter_val != s['id']):
							speciese.remove(species)
		return speciese, 200
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
		parser.add_argument('image', type=str, required=True, help="Image cannot be blank!")
		parser.add_argument('countries_id', type=int, action='append', required=True, help="Country(ies) id cannot be blank!")
		parser.add_argument('genuses_id', type=int, action='append', required=True, help="Genus(es) id cannot be blank!")
		parser.add_argument('description', type=str, required=True, help="Description id cannot be blank!")
		data = parser.parse_args()
		exist_name = self.db.row("SELECT name FROM specieses WHERE name = :name", {"name": data['name']})
		if(len(exist_name) == 0):
			species_id = self.db.row("INSERT INTO specieses (name, image, description) VALUES (:name, :image, :description) RETURNING id", {'name': data['name'], 'image': data['image'], 'description': data['description']})
			genuses = Genuses()
			error = False
			for i in data['genuses_id']:
				genus_id = genuses.get(i)[0]
				if(genus_id['status'] == 404):
					error = True
					no_id = i
					break
			if(error is False):
				countries = Countries()
				for i in data['countries_id']:
					country_id = countries.get(i)[0]
					if(country_id['status'] == 404):
						error = True
						no_id = i
						break
			else:
				answer = {"data": "This id of genuses - "+str(no_id)+" not exist!", "status": 400}
				return answer, 400
			if(error is False):
				species = self.db.row("SELECT * FROM specieses WHERE id = :id", species_id[0])
				for i in data['genuses_id']:
					self.db.query("INSERT INTO genuses_specieses (genus_id, species_id) VALUES (:genus_id, :species_id)", {"genus_id": i, "species_id": species_id[0]['id']})
				for i in data['countries_id']:
					self.db.query("INSERT INTO countries_specieses (country_id, species_id) VALUES (:country_id, :species_id)", {"country_id": i, "species_id": species_id[0]['id']})
				genuses = self.db.row("SELECT genuses.id, genuses.name FROM genuses_specieses RIGHT JOIN genuses ON genuses_specieses.genus_id = genuses.id WHERE species_id = :id", {'id': species_id[0]['id']})
				countries = self.db.row("SELECT countries.id, countries.name FROM countries_specieses RIGHT JOIN countries ON countries_specieses.country_id = countries.id WHERE species_id = :id", {'id': species_id[0]['id']})
				species[0]['genuses'] = genuses
				species[0]['countries'] = countries
				answer = {"data": species, "status": 201}
				return answer, 201
			else:
				answer = {"data": "This id of countries - "+str(no_id)+" not exist!", "status": 400}
				return answer, 400
		else:
			answer = {"data": "This name already exist!", "status": 400}
			return answer, 400
	def put(self, id):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str)
		parser.add_argument('image', type=str)
		parser.add_argument('countries_id', type=int, action='append')
		parser.add_argument('genuses_id', type=int, action='append')
		parser.add_argument('description', type=str)
		data = parser.parse_args()
		exist_name = self.db.row("SELECT name FROM specieses WHERE name = :name", {"name": data['name']})
		if(data['name'] is None or len(exist_name) == 0):
			if(len(dict(filter(lambda elem: elem[1] is not None, data.items()))) == 0):
				answer = {'data': "Bad request", 'status': 400}
				return answer, 400
			if(data['name'] is not None):
				self.db.query("UPDATE specieses SET name = :name WHERE id = :id", {'id': id, 'name': data['name']})
			if(data['image'] is not None):
				self.db.query("UPDATE specieses SET image = :image WHERE id = :id", {'id': id, 'image': data['image']})
			if(data['description'] is not None):
				self.db.query("UPDATE specieses SET description = :description WHERE id = :id", {'id': id, 'description': data['description']})
			if(data['countries_id'] is not None):
				self.db.query("DELETE FROM countries_specieses WHERE species_id = :id", {'id': id})
				countries_q = ""
				for country in data['countries_id']:
					if(data['countries_id'][-1] == country):
						countries_q += "("+str(country)+","+str(id)+")"
					else:
						countries_q += "("+str(country)+","+str(id)+"), "
				self.db.query("INSERT INTO countries_specieses (country_id, species_id) VALUES " + countries_q)
			if(data['genuses_id'] is not None):
				self.db.query("DELETE FROM genuses_specieses WHERE species_id = :id", {'id': id})
				genuses_q = ""
				for genus in data['genuses_id']:
					if(data['genuses_id'][-1] == genus):
						genuses_q += "("+str(genus)+","+str(id)+")"
					else:
						genuses_q += "("+str(genus)+","+str(id)+"), "
				self.db.query("INSERT INTO genuses_specieses (genus_id, species_id) VALUES " + genuses_q)
			return self.get(id)
		else:
			answer = {"data": "This name already exist!", "status": 400}
			return answer, 400
	def delete(self, id):
		is_id = self.get(id)[0]
		if(is_id['status'] != 404):
			self.db.query("DELETE FROM specieses WHERE id = :id", {"id": id})
			self.db.query("DELETE FROM genuses_specieses WHERE species_id = :id", {'id': id})
			self.db.query("DELETE FROM countries_specieses WHERE species_id = :id", {'id': id})
			answer = {"data": "Species with id "+str(id)+" is deleted.", 'status': 200}
			return answer, 200
		else:
			answer = {"data": "Bad request", 'status': 400}
			return answer, 400
			

