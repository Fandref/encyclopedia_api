from flask_restful import Resource, reqparse
from .world_areas import WoldAreas
from db import Db

class Countries(Resource):
	db = Db("encyclopedia", "postgres", "", '127.0.0.1')
	def get(self, id = 0):
		if(id != 0):
			country = self.db.row("SELECT * FROM countries WHERE id = :id", {"id": id})
		else:
			country = self.db.row("SELECT * FROM countries")
		if(len(country) > 0):
			answer = {"data": country, 'status': 200}
			return answer, 200
		else:
			answer = {"data": [], 'status': 404}
			return answer, 404
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
		parser.add_argument('world_area_id', type=int, action='append', required=True, help="World area id cannot be blank!")
		parser.add_argument('description', type=str, required=True, help="Description id cannot be blank!")
		data = parser.parse_args()
		if(len(data) != 0):
			if(data['name'] is not None and data['world_area_id'] is not None and data['description'] is not None):
				wad = WoldAreas()
				world_a_id = wad.get(data['world_area_id'])[0]
				if(int(world_a_id['status']) != 404):
					country_id = self.db.row("INSERT INTO countries (name, world_area_id, description) VALUES (:name, :world_area_id, :description) RETURNING id", data)
					country = self.db.row("SELECT * FROM countries WHERE id = :id", country_id[0])
					answer = {"data": country, "status": 201}
					return answer, 201
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
		parser.add_argument('world_area_id')
		parser.add_argument('description')
		data = parser.parse_args()
		data['id'] = id
		if(len(data) != 0 and id is not None):
			is_id = self.get(id)[0]
			if(is_id['status'] != 404):
				if(data['name'] is not None and data['world_area_id'] is not None and data['description'] is not None):
					self.db.query("UPDATE countries SET name = :name, world_area_id = :world_area_id, description = :description WHERE id = :id", data)
				elif(data['name'] is not None and data['world_area_id'] is not None):
					self.db.query("UPDATE countries SET name = :name, world_area_id = :world_area_id WHERE id = :id", data)
				elif(data['name'] is not None and data['description'] is not None):
					self.db.query("UPDATE countries SET name = :name, description = :description WHERE id = :id", data)
				elif(data['world_area_id'] is not None and data['description'] is not None):
					self.db.query("UPDATE countries SET world_area_id = :world_area_id, description = :description WHERE id = :id", data)
				elif(data['name'] is not None):
					self.db.query("UPDATE countries SET name = :name WHERE id = :id", data)
				elif(data['world_area_id'] is not None):
					self.db.query("UPDATE countries SET world_area_id = :world_area_id WHERE id = :id", data)
				elif(data['description'] is not None):
					self.db.query("UPDATE countries SET description = :description WHERE id = :id", data)
				country = self.db.row("SELECT * FROM countries WHERE id = :id", {"id": id})
				answer = {"data": country, "status": 201}
				return answer, 201
			else:
				answer = {"data": "Bad request", "status": 400}
				return answer, 400
		else:
			answer = {"data": "Bad request", "status": 400}
			return answer, 400
	def delete(self, id):
		is_id = self.get(id)[0]
		if(is_id['status'] != 404):
			self.db.query("DELETE FROM countries WHERE id = :id", {"id": id})
			answer = {"data": "Country with id "+id+" is deleted.", 'status': 200}
			return answer, 200
		else:
			answer = {"data": "Bad request", 'status': 400}
			return answer, 400