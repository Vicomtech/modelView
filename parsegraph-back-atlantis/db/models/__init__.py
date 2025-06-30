
import numpy as np
from db import BaseModelMixin, EVAXPLAINIFY_API
from sqlalchemy.orm import Mapped, mapped_column
import  sqlalchemy as sqla
import requests

class Model(BaseModelMixin):
  __tablename__ = "models_table"
  id: Mapped[int] = mapped_column(sqla.Integer, primary_key=True)
  Name: Mapped[str] = mapped_column(sqla.String, nullable=False)
  Description: Mapped[str] = mapped_column(sqla.String)
  NumberLayers:Mapped[int] = mapped_column(sqla.Integer)
  __table_args__ = (sqla.UniqueConstraint("Name"),)

  @classmethod
  def numberBlocks(cls,model:str) -> int:
    """return the number of blocks of a model"""
    stm = sqla.select(Filter.Model, sqla.func.count(sqla.distinct(Filter.Block)).label("NumBlocks")).where(Filter.Model.like(model)).group_by(Filter.Model)
    result = db.session.execute(stm).one()
    return tuple(result)[1]
  
  @classmethod
  def ModelExists(cls, modelname:str) -> bool:
    result = cls.get_first(Name=modelname)
    return True if result != None else False

class Layer(BaseModelMixin):
  __tablename__ = "layers_table"
  id: Mapped[str] = mapped_column(sqla.String, primary_key=True)
  Model: Mapped[str] = mapped_column(sqla.String, nullable=False)
  Block: Mapped[str] = mapped_column(sqla.String, nullable=False)
  LayerInBlock:Mapped[str] = mapped_column(sqla.String, nullable=False)
  LayerType: Mapped[str] = mapped_column(sqla.String)
  NumberNodes:Mapped[int] = mapped_column(sqla.Integer)

  @classmethod
  def ModelExists(cls, modelname:str) -> bool:
    result = cls.get_first(Model=modelname)
    return True if result != None else False
  
  @classmethod
  def getstructure(cls, modelname:str) -> list:
    global API
    if (modelname == "default"):
      url = f"{EVAXPLAINIFY_API}/model_structure/"
      response = requests.get(url).json()
      elemlist = []
      for key, value in response.items():
        for layer, elem in value.items():
          elemlist.append({"Model":"default", "id":f"default_{elem['n_layer']}", "Block":key, "LayerInBlock":layer, "LayerType": elem["type"], "NumberNodes":elem["n_nodes"]})
      cls.bulk_insert(elemlist)
      return elemlist
    else:
      raise Exception('No model with given name')
    
class Filter(BaseModelMixin):
  __tablename__ = "filters_table"
  id: Mapped[int] = mapped_column(sqla.Integer, primary_key=True)
  Model: Mapped[str] = mapped_column(sqla.String)
  Layer: Mapped[str] = mapped_column(sqla.String, sqla.ForeignKey("layers_table.id"))
  Block: Mapped[str] = mapped_column(sqla.String, nullable=False)
  FilterInLayer: Mapped[int] = mapped_column(sqla.Integer)
  PosX: Mapped[float] = mapped_column(sqla.Float, nullable=False, default=0)
  PosY: Mapped[float] = mapped_column(sqla.Float, nullable=False, default=0)

  @classmethod
  def ModelExists(cls, modelname:str) -> bool:
    result = cls.get_first(Model=modelname)
    return True if result != None else False

  @classmethod
  def updatePositions(cls, modelname:str) -> list:
    global API
    if (modelname == "default"):
      url = f"{EVAXPLAINIFY_API}/model_structure/"
      response = requests.get(url).json()
      elemlist = []
      for block, layers in response.items():
        lcount = 1
        for elem in layers.values():
          sep = int(300)
          layerx =  round(10000 / len(layers.keys()))
          for i in range(1, elem["n_nodes"]+1):
            Layer = f"default_{elem['n_layer']}"
            posX = np.random.uniform((lcount -1) * layerx + sep, lcount * layerx - sep)
            posY = np.random.uniform(sep, 5000 - sep)
            elemlist.append({"Model": "default", "Layer":Layer, "Block": block, "FilterInLayer":i, "PosX": posX, "PosY": posY})
          lcount = lcount + 1
      cls.bulk_insert(elemlist)
      return elemlist
    else:
      raise Exception('No model with given name')

