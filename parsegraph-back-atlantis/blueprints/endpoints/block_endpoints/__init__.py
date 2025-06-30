
from flask import request
from flask_restx import Namespace, Resource, fields, abort
from db.models import Filter, Layer
from db import db
import sqlalchemy as sqla

namespace = Namespace('Blocks', 'endpoint to manage queries related to a block of the behaviour graph')

nblock = fields.Integer(description="The number of blocks in a model")

blockname = fields.List (fields.String(description="BlockName"))

@namespace.route("")
class Blocklist(Resource):
  '''Get block list of an specific model'''

  @namespace.response(200, "success", blockname)
  @namespace.response(500, 'internal server error')
  @namespace.response(400, "Model with given name cannot been found")
  @namespace.param(name="model", description="Name of the model the blocks belongs to", _in="query", required=False, example="default")
  def get(self):
      '''Lists all blocks that belong to a specific model'''
      model = request.args.get('model') if 'model' in request.args else 'default'
      if Layer.ModelExists(model):
        query = sqla.select(Layer.Block.distinct()).where(Layer.Model == model)
        res = db.session.execute(query).all()
        result = []
        for r in res:
          result.append(r[0] )
      else: 
        el = Layer.getstructure(model)
        Filter.updatePositions(model)
        result = []
        for r in el:
          if len(result) == 0 or r['Block'] != result[len(result)-1]:
            result.append(r['Block']) 
      return result

@namespace.route("/count")
class Count(Resource):
  """gets the number of blocks in a model"""

  @namespace.response(404, "model not found")
  @namespace.param(name="model", description="Name of the model the block belongs to", _in="query", example="default_model")
  @namespace.response(200, "success", nblock)
  @namespace.response(500, "Internal server error")
  def get(self):
    """Get the number of blocks in a model"""
    model = request.args.get('model') if 'model' in request.args else 'default'
    if model != 'default':
      abort(400, 'missing parameter, you need to specify the name of a model')
    else:
      try:
        query = sqla.select(sqla.func.count(Layer.Block.distinct())).where(Layer.Model == model)
        res = db.session.execute(query).first()
        return res[0]
      except:
        abort(404, "model not found")