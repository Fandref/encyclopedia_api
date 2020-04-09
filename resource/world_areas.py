from flask_restful import Resource, reqparse
from db import Db

class WoldAreas(Resource):
	db = Db("encyclopedia", "postgres", "", '127.0.0.1')
	def get(self, id=0):
		if(id != 0):
			world_area = self.db.row("SELECT name, description FROM world_areas WHERE id = :id", {"id": id})
		else:
			world_area = self.db.row("SELECT id, name, description FROM world_areas")
		if(len(world_area) > 0):
			answer = {"data": world_area, 'status': 200}
			return answer, 200
		else:
			answer = {"data": [], 'status': 404}
			return answer, 404
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
		parser.add_argument('description', type=str, required=True, help="Description id cannot be blank!")
		data = parser.parse_args()
		if(len(data) != 0):
			if(data['name'] is not None and data['description'] is not None):
				world_area_id = self.db.row("INSERT INTO world_areas (name, description) VALUES (:name, :description) RETURNING id", data)
				world_area = self.db.row("SELECT * FROM world_areas WHERE id = :id", world_area_id[0])
				answer = {"data": world_area, "status": 201}
				return answer, 201
			else:
				answer = {"data": "Bad request", "status": 400}
				return answer, 400
		else:
			answer = {"data": "Bad request", "status": 400}
			return answer, 400
	def put(self, id):
		parser = reqparse.RequestParser()
		parser.add_argument('name')
		parser.add_argument('description')
		data = parser.parse_args()
		data['id'] = id
		if(len(data) != 0 and id is not None):
			is_id = self.get(id)[0]
			if(is_id['status'] != 404):
				if(data['description'] is not None and data['name'] is not None):
					world_area_id = self.db.query("UPDATE world_areas SET name = :name, description = :description WHERE id = :id", data)
				if(data['name'] is not None):
					world_area_id = self.db.query("UPDATE world_areas SET name = :name WHERE id = :id", data)
				elif(data['description'] is not None):
					world_area_id = self.db.query("UPDATE world_areas SET description = :description WHERE id = :id", data)
				world_area = self.db.row("SELECT * FROM world_areas WHERE id = :id", {"id": id})
				answer = {"data": world_area, "status": 201}
				return answer, 201
			else:
				answer = {"data": "Bad request", 'status': 400}
				return "Bad request", 400
		else:
			answer = {"data": "Bad request", 'status': 400}
			return "Bad request", 400
	def delete(self, id):
		is_id = self.get(id)[0]
		if(is_id['status'] != 404):
			self.db.query("DELETE FROM world_areas WHERE id = :id", {"id": id})
			return f"World area with id {id} is deleted.", 200
		else:
			answer = {"data": "Bad request", 'status': 400}
			return "Bad request", 400