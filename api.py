from flask import Flask, jsonify
from flask_restful import Api


from resource.specieses import Specieses
from resource.world_areas import WoldAreas
from resource.countries import Countries
from resource.domains import Domains
from resource.kinds import Kinds
from resource.types import Types
from resource.sub_types import SubTypes
from resource.classes import Classes
from resource.sub_classes import SubClasses
from resource.ordos import Ordos
from resource.familias import Familias
from resource.genuses import Genuses

app = Flask(__name__)
api = Api(app)


api.add_resource(Specieses, "/specieses", "/specieses/", "/specieses/<int:id>")
api.add_resource(WoldAreas, "/world-areas", "/world-areas/", "/world-areas/<int:id>")
api.add_resource(Countries, "/countries", "/countries/", "/countries/<int:id>")
api.add_resource(Domains, "/domains", "/domains/", "/domains/<int:id>")
api.add_resource(Kinds, "/kinds", "/kinds/", "/kinds/<int:id>")
api.add_resource(Types, "/types", "/types/", "/types/<int:id>")
api.add_resource(SubTypes, "/sub-types", "/sub-types/", "/sub-types/<int:id>")
api.add_resource(Classes, "/classes", "/classes/", "/classes/<int:id>")
api.add_resource(SubClasses, "/sub-classes", "/sub-classes/", "/sub-classes/<int:id>")
api.add_resource(Ordos, "/ordos", "/ordos/", "/ordos/<int:id>")
api.add_resource(Familias, "/familias", "/familias/", "/familias/<int:id>")
api.add_resource(Genuses, "/genuses", "/genuses/", "/genuses/<int:id>")


if __name__ == '__main__':
    app.run(debug=True)