
from flask import request
from flask_restx import Namespace, Resource, fields, abort
from db.models import Filter, Layer
from db import db

namespace = Namespace('Layers', 'endpoint to manage queries related to layers')

layer = namespace.model("Layer", {
  'id': fields.String (attribute = "id", required=False, description='Layer unique id'),
  'layer': fields.String(attribute = "LayerInBlock",required=True, description='Model name'),
  'type': fields.String(attribute = "LayerType",required=True, description='Block name'),
  'n_nodes': fields.Integer(attribute = "NumberNodes",required=True, description='Number of nodes in layer'),
})

@namespace.route("/inblock")
class ImageInterpreted(Resource):
  '''Get layer info of a given block'''
  
  @namespace.marshal_list_with(layer)
  @namespace.response(500, 'internal server error')
  @namespace.response(400, 'missing parameter, you need to specify the model and the block')
  @namespace.response(404, "block not found")
  @namespace.param(name="model", description="Name of the model the node belongs to", _in="query", required=True, default="default")
  @namespace.param(name="block", description="Name of the block the node belongs to", _in="query", required=True, default="block_1")
  def get(self):
    model = request.args.get('model') if 'model' in request.args else ''
    block = request.args.get('block') if 'block' in request.args else ''
    if model == '' or block == '':
      abort(400, 'missing parameter, you need to specify the model and the block')
    if not Layer.ModelExists(model):
        Layer.getstructure(model)
        Filter.updatePositions(model)
    result = db.session.query(Layer.id, Layer.LayerInBlock, Layer.LayerType, Layer.NumberNodes).filter(Layer.Block == block).filter(Layer.Model == model).all()
    if len(result) < 1:
      abort(404, "block not found")
    return result