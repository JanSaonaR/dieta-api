from flask import request, Blueprint
from flask_restful import Api, Resource
from app.common.error_handling import ObjectNotFound 

diets_v1_0_bp = Blueprint('diets_v1_0_bp', __name__)

api = Api(diets_v1_0_bp)


class DietListResource(Resource):
    def get(self):
        args = request.args
        print(args)
        diet = {
                "age": int(args['age']),
                "weight": float(args['weight']),
                "height": int(args['height'])
                }
        if diet is None:
            raise ObjectNotFound('No existen dietas')
        return diet

api.add_resource(DietListResource, '/api/v1.0/diets',\
        endpoint='diet_list_resource')
