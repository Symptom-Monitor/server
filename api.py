import flask
from flask import jsonify
from flask_cors import CORS, cross_origin
from algorithms import all

app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config["DEBUG"] = True

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
  # Find algo
  print(algo_id)
  algo = None
  for a in all.algorithms:
    print(a)
    if a.id == algo_id:
      algo = a
      break
  
  if algo is None:
    return 'algorithm doesn\'t exist', 400

  res = algo.process()

  return jsonify({"good": True, "str": res})

app.run()
