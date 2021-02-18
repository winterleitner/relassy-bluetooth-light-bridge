from flask import Flask, render_template, jsonify, Response, request
#from flask_cors import CORS
from light_handler import scan, Light
app = Flask(__name__)
#CORS(app)

lights = []

@app.route('/')
def hello_world():
    print(lights)
    return render_template('index.html', lights=scan())


@app.route("/scan")
def scan_lights():
    lights = scan()
    objects = []
    for l in lights:
        objects.append(l.to_object())
    return jsonify(objects)

@app.route("/light", methods = ['GET'])
def get_light():
    address = request.args.get("address")
    light = Light("random", address)
    status = light.getLight()
    return jsonify(status)

@app.route('/light', methods = ['POST'])
def set_light():
    address = request.args.get("address")
    blue = request.json['blue']
    white = request.json['white']
    light = Light("random", address)
    light.setLight(blue, white)
    return jsonify({"status": "ok"})