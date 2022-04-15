from flask import Blueprint
from flask_restx import Api
from app.common.globals import init

from .namespace_diets import api as ns1

diets_v1_0_bp = Blueprint('diets_v1_0_bp', __name__, url_prefix='/api/v1.0')


@diets_v1_0_bp.before_app_first_request
def getData():
    init()


api = Api(
    diets_v1_0_bp,
    title='Dieta Perfecta API',
    version='1.0',
    description='API que permite obtener dietas según los requerimientos\
            de niños de entre 6 y 12 años.',
    doc='/doc',
    # Captura todos los errores 404
    catch_all_404s=True
)

api.add_namespace(ns1)
