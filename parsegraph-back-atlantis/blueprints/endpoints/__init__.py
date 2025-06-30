from flask import Blueprint
from flask_restx import Api
from blueprints.endpoints.block_endpoints import namespace as block_ns
from blueprints.endpoints.filter_endpoints import namespace as filter_ns
from blueprints.endpoints.layer_endpoints import namespace as layer_ns
from blueprints.endpoints.image_endpoints import namespace as im_ns

blueprint = Blueprint('documented_api', __name__, url_prefix='/viz_api')

api_extension = Api(
    blueprint,
    title='Evaxplanify visualization API',
    version='1.0',
    description='Backend to manage the visual display of a behaviour graph created by Evaxplainify',
    doc='/doc'
)

api_extension.add_namespace(block_ns)
api_extension.add_namespace(filter_ns)
api_extension.add_namespace(layer_ns)
api_extension.add_namespace(im_ns)