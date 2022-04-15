import warnings

from flask import request
from flask_restx import Namespace, Resource, fields
from pandas.core.common import SettingWithCopyWarning

from app.common.error_handling import ObjectNotFound
from app.diets.models import Child, Diet
import app.common.globals

warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)

api = Namespace('diets', 'Diets related enpoints')

# MODELS

child_model = api.model('Infante', {
    'age': fields.Integer(
        required=True,
        min=6, max=12,
        description='Edad del niño',
        example=6),
    'weight': fields.Float(
        required=True,
        description='Peso del niño',
        example=35.0),
    'height': fields.Integer(
        required=True,
        description='Altura del niño',
        example=175),
    'activity': fields.String(
        required=True,
        description='Nivel de actividad del niño',
        example='sedentario'),
    'days': fields.Integer(
        required=True,
        min=1,
        description='Número de días que la dieta durará',
        example=1),
    'sex': fields.String(
        required=True,
        description='Sexo del niño',
        example='F'),
    'preference': fields.List(fields.String,
                              description='Ingredientes que prefiere el niño',
                              example=["POLLO", "PAPA", "HUEVO"])
})

refoods_model = api.model('Comidas Opcionales', {
    'type': fields.String(
        required=True,
        example='Cena',
        description='Horario para el que quiere las nuevas comidas'),
    'calories': fields.Float(
        required=True,
        example=400.0,
        description='Calorías que tienen que cumplir las comidas')
})


str_str = api.model('Respuesta índice - texto', {
    'index': fields.String(),
    'content': fields.String()
})

str_int = api.model('Respuesta índice - entero', {
    'index': fields.String(),
    'content': fields.Integer()
})

str_float = api.model('Respuesta índice - flotante', {
    'index': fields.String(),
    'content': fields.Integer()
})

str_lst = api.model('Respuesta índice - lista', {
    'index': fields.String(),
    'content': fields.List(fields.String())
})


diet_list_rsp = api.model('Dietas', {
    'Alimento': fields.Nested(str_str),
    'Proteinas': fields.Nested(str_float),
    'Grasas': fields.Nested(str_float),
    'Carbohidratos': fields.Nested(str_float),
    'Cantidad_Gramos_Consumir': fields.Nested(str_int),
    'Total_Calorias': fields.Nested(str_int),
    'Ingredientes': fields.Nested(str_lst),
    'Nivel_Preferencia': fields.Nested(str_int),
    'Image_url': fields.Nested(str_str),
    'Tipo': fields.Nested(str_str),
})

# CONTROLERS


@api.route('')
class DietListResource(Resource):
    @api.expect(child_model)
    @api.response(code=200,
                  description='El API responde con la lista de los alimentos,\
                          sus macronutrientes e ingredientes.',
                  model=diet_list_rsp)
    def post(self):
        args = request.get_json()

        keys = ['age', 'weight', 'height', 'activity', 'sex', 'days',
                'preference']

        for key in keys:
            if key not in args.keys():
                raise ObjectNotFound('Falta un campo en la petición')

        age = args[keys[0]]
        weight = args[keys[1]]
        height = args[keys[2]]
        activity = args[keys[3]]
        sex = args[keys[4]]
        days = args[keys[5]]
        preference = args[keys[6]]

        child = Child(age, weight, height, activity, sex, preference)

        data = app.common.globals.data
        diet = Diet(child, data)

        dietList = None
        dietList = diet.getDiets(days)

        if dietList is None:
            raise ObjectNotFound('No existen dietas')

        return dietList


@api.route('/refoods')
class recomendation(Resource):
    @api.expect(refoods_model)
    @api.response(code=200,
                  description='El API responde con la lista de los alimentos,\
                          sus macronutrientes e ingredientes.',
                  model=diet_list_rsp)
    def post(self):
        args = request.get_json()

        keys = ['type', 'calories']
        for key in keys:
            if key not in args.keys():
                raise ObjectNotFound('Falta un campo en la petición')

        type = args[keys[0]]
        calories = args[keys[1]]

        child = Child(type, calories)
        data = app.common.globals.data
        diet = Diet(child, data)

        dietList = None
        dietList = diet.get3foods()

        if dietList is None:
            raise ObjectNotFound('No existen dietas')

        return dietList
