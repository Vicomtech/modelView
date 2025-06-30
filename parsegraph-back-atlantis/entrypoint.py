import json
from flask import Flask
from flask_cors import CORS
import numpy as np
from blueprints.endpoints import blueprint as endpoints
from db import db
from dotenv import load_dotenv
import os
from db.models import Layer, Filter, Model
import requests

app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.
load_dotenv()
dbuser = os.getenv("DB_USER") or "db_user"
dbpass = os.getenv("DB_PASSWORD") or "db_p4ssw0rd"
dbname = os.getenv("DB_NAME") or "db_atlantis"
dbport = os.getenv("DB_PORT") or "5433"
dbreset = os.getenv("DB_RESET") == "True" or False
dbhost =  os.getenv("DB_HOST") or "localhost"


app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = f"postgresql://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}"
app.config['RESTPLUS_MASK_SWAGGER'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

API = f'http://{os.getenv("EVAPI_HOST") or "localhost"}:{os.getenv("EVAPI_PORT") or "8889"}'

def reloadDB():
  with app.app_context():
    if(dbreset):
      db.drop_all()
    db.create_all()
    with open('envconfig.json') as f:
      conf = json.load(f)

    mode = conf["Mode"]["value"]

    if mode == "REMOTE":
      struct = requests.get(f"{API}/model_structure/")
      data = struct.json()
      model= str(conf["Envname"])
    else:
      modelfile = str(conf["localconf"]["modelfile"])
      model = modelfile.split(".")[0]
      with open(modelfile) as f:
        data = json.load(f)
    
    blocklist = list(data.keys())
    layers = list()
    nodes = list()

    Ml = {"Name": model, "Description":"", "NumberLayers": len(blocklist)}
    if  not Model.ModelExists(model):
      Model.bulk_insert(Ml)

      for block in blocklist:
        layerlist = list(data[block].keys())
        sep = int(300)
        layerx =  round(10000 / len(layerlist))
        lcount = 1
        for layer in layerlist:
          nodecount = data[block][layer]["n_nodes"]
          layers.append({"id": f"{model}_{data[block][layer]['n_layer']}", "Model": model, "LayerInBlock":f"layer_{lcount}", "Block": block, "LayerType": data[block][layer]["type"], "NumberNodes":nodecount})
          for i in range(1, nodecount+1):
            posX = np.random.uniform((lcount -1) * layerx + sep, lcount * layerx - sep)
            posY = np.random.uniform(sep, 5000 - sep)
            nodes.append({"Model": model, "Layer":f"{model}_{data[block][layer]['n_layer']}", "Block": block, "FilterInLayer":i, "PosX": posX, "PosY": posY})
          lcount = lcount + 1
      
      Layer.bulk_insert(layers)
      Filter.bulk_insert(nodes)

print ("init db")
db.init_app(app)
print ("done init db")



app.register_blueprint(endpoints)
print("resetting db...")
reloadDB()
print("done")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)