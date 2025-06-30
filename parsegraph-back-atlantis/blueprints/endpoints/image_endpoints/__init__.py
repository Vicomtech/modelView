
import io
import json
import time
from typing import Optional
from flask import request
import flask
from flask_cors import cross_origin
from flask_restx import Namespace, Resource, fields, abort, reqparse
import requests
from werkzeug.datastructures import FileStorage
from PIL import Image as im

def multiple_file_param(arg_name: str, ns: Namespace, parser: Optional[reqparse.RequestParser] = None) -> reqparse.RequestParser:
    if not parser:
        parser = ns.parser()
    parser.add_argument(arg_name, type=FileStorage, location='files', required=True, help='image to send')
    return parser

namespace = Namespace('ImageSelection', 'endpoint to manage queries related to image selection')
croppedfaces = namespace.model('croppedfaces', {
  'faces': fields.List(fields.List(fields.List(fields.List(fields.Integer))), description='List of cropped faces as matrices of shape (3,380,380)')
})

URL = ' https://deepfakes-detection.atlantis.lab.synelixis.com/image_crop_faces/'
headers = {'api-key':'a_secret_key'}
file_param =  multiple_file_param(arg_name='file', ns=namespace)

@namespace.route("/crop")
class Cropfaces(Resource):
  '''Get layer info of a given block'''
  @namespace.expect(file_param)
  @namespace.response(200, "success", croppedfaces)
  @namespace.response(500, 'internal server error')
  @namespace.response(400, 'Missing file')
  def post(self):
    '''Send image with faces to receive them cropped'''
    image = request.files.get('file')
    if (image):
      print('Image received, starting to process')
      buf = io.BytesIO()
      pilim = im.open(image)
      pilim.save(buf, format='JPEG')
      byte_im = buf.getvalue()

      files = {'file': ('image.jpg', io.BytesIO(byte_im), 'image/jpeg')}

      try:
          response = requests.post(url=URL, files=files, headers=headers)
          task = response.json()
      except requests.exceptions.RequestException as e:
          print("Error during request:", e)
      except json.JSONDecodeError as e:
          print("Error decoding JSON:", e)
          print("Raw Response Content:", response.content)  # Print content on JSONDecodeError

      tid = task["task_id"]

      data = {"task_id":tid, 'status':'pending'}
      iterattions = 0
      while 'status' in data.keys() and data['status'] != 'failed':
        print(f"({iterattions}) task_id:{data['task_id']}, status:{data['status']}")
        data = requests.get(url=URL+tid, headers=headers).json()
        iterattions = iterattions + 1


      if 'status' in data.keys():
        abort(500, f"Internal server error. An error ocurred during crop.")
      
      else:
         images =flask.jsonify( {
            'faces': data["faces"]
          })
         images.headers.add('Access-Control-Allow-Origin', '*')
         return images
    else:
      abort(400, 'Missing file')