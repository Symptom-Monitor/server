# Import env vars
from dotenv import load_dotenv
load_dotenv()

import os
import uuid
import flask
from flask import jsonify, request
from flask.helpers import send_file, send_from_directory
from flask_cors import CORS, cross_origin
from algorithms import all
from simulation import map

app = flask.Flask(__name__, static_url_path='')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = os.path.join(os.getenv('DATA_DIR'), 'uploads')

# Make folders if they don't exist
generated_dir = os.path.join(os.getenv('DATA_DIR'), 'generated');
if not os.path.exists(generated_dir):
  os.makedirs(generated_dir)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
  os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/map', methods=['GET'])
@cross_origin()
def get_map():
  x = float(request.args.get('x'))
  y = float(request.args.get('y'))
  alpha = float(request.args.get('alpha'))
  beta = float(request.args.get('beta'))
  gamma = float(request.args.get('gamma'))

  video_path = map.simulate(x, y, alpha, beta, gamma)

  return send_file(video_path, mimetype='video/mp4')

@app.route('/static/<path:path>')
@cross_origin()
def send_static(path):
  return send_from_directory('public', path)

@app.route('/algorithms', methods=['GET'])
@cross_origin()
def algorithms():
  algos = []

  for algo in all.algorithms:
    algos.append({"id": algo.id, "name": algo.name})

  return jsonify(algos)

@app.route('/algorithms/<algo_id>', methods=['POST'])
@cross_origin()
def process_video(algo_id):
  if 'file' not in request.files:
    return 'missing file', 400
  
  file = request.files['file']
  if file.filename == '':
    return 'missing file', 400

  location = None

  if file:
    filename = uuid.uuid4().hex
    location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(location)

  # Find algo
  algo = None
  for a in all.algorithms:
    if a.id == algo_id:
      algo = a
      break
  
  if algo is None:
    return 'algorithm doesn\'t exist', 400

  res = algo.process(location)

  # Delete uploaded video
  os.remove(location)

  return jsonify(res)

app.run()
