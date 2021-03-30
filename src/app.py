from flask import Flask, render_template, jsonify, Response, request
from light_handler import scan, Light
app = Flask(__name__)

lights = []

# serves react frontend, requires index.html in /templates and /react/build/static in /static
@app.route('/')
def home():
    print(lights)
    return render_template('index.html')


@app.route("/scan")
def scan_lights():
    """
    Starts the search for bluetooth lights

    :return: a list of found lights as JSON
    """
    lights = scan()
    objects = []
    for l in lights:
        objects.append(l.to_object())
    return jsonify(objects)


@app.route("/light", methods = ['GET'])
def get_light():
    """
    gets the current light state(blue/white)

    :return: the status as json
    """
    address = request.args.get("address")
    light = Light("random", address)
    status = light.getLight()
    return jsonify(status)


@app.route('/light', methods = ['POST'])
def set_light():
    """
    sets a light's state

    :return: status: ok for success
    """
    address = request.args.get("address")
    blue = request.json['blue']
    white = request.json['white']
    light = Light("random", address)
    light.setLight(blue, white)
    return jsonify({"status": "ok"})


# shortcut for my personal lights. Delete this or insert your Light's MAC addresses.
@app.route('/h5-turn-off')
def turn_all_off():
    addresses = ["4c:24:98:94:42:07", "4c:24:98:94:10:8f", "4c:24:98:d2:19:98"]

    for a in addresses:
        try:
            light = Light("random", a)
            light.turn_off()
        except:
            print(f"Failed toggling {a}")
    return jsonify({"status": "ok"})


# shortcut for my personal lights. Delete this or insert your Light's MAC addresses.
@app.route('/h5-turn-on')
def turn_all_on():
    addresses = ["4c:24:98:94:42:07", "4c:24:98:94:10:8f", "4c:24:98:d2:19:98"]

    for a in addresses:
        try:
            light = Light("random", a)
            light.turn_on()
        except:
            print(f"Failed toggling {a}")
    return jsonify({"status": "ok"})
