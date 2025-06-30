from flask import request
from flask_restx import Namespace, Resource, fields, abort
from db.models import Filter, Layer
from db import db

namespace = Namespace('Nodes', 'endpoint to manage queries related to the nodes of the behaviour graph')

node = namespace.model("Node", {
  'id': fields.Integer (attribute = "id", required=False, description='node id'),
  'positionX': fields.Float (attribute = "PosX", required=True, description='Node position on the X axis'),
  'positionY':  fields.Float(attribute = "PosY",required=True, description='Node position on the Y axis'),
  'model': fields.String(attribute = "Model",required=True, description='Model name'),
  'layer': fields.String(attribute = "Layer",required=True, description='Layer name'),
  'block': fields.String(attribute = "Block",required=True, description='Block name'),
  'filterinlayer': fields.Integer (attribute = "FilterInLayer", required=True, description='number in layer'),
})

@namespace.route("")
class NodeList(Resource):
  '''Gets and updates the list of nodes belonging to an specific block'''

  @namespace.marshal_list_with(node)
  @namespace.response(500, 'internal server error')
  @namespace.response(400, 'missing parameter, you need to specify the model, the block and the chosen image')
  @namespace.response(404, "block not found")
  @namespace.param(name="model", description="Name of the model the node belongs to", _in="query", required=True, default="default")
  @namespace.param(name="block", description="Name of the block the node belongs to", _in="query", required=True, default="block_1")
  def get(self):
      '''Lists all nodes that belong to a specific block of a model'''
      model = request.args.get('model') if 'model' in request.args else 'default'
      block = request.args.get('block') if 'block' in request.args else 'block_1'
      if model == '' or block == '':
        abort(400, 'missing parameter, you need to specify the model and the block')
      if not Filter.ModelExists(model):
        Layer.getstructure(model)
        Filter.updatePositions(model)
      result = (
        db.session.query(Filter)
        .filter(Filter.Block == block)
        .filter(Filter.Model == model)
        .all()
        )
      if len(result) < 1:
        abort(404, "block not found")
      return result