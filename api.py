import os
import uuid
import flask
from flask import jsonify, request
from flask_cors import CORS, cross_origin
from algorithms import all

app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = './uploads'

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
