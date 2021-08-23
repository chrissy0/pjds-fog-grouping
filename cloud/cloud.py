from flask import Flask
from flask import request

app = Flask(__name__)


clusters = {}


def response_object(message=None, code=200):
    res = {"response": clusters}
    if message:
        res["message"] = message
    return res, code


@app.route('/register-cluster', methods=['POST'])
def register_cluster():
    ip = request.form["ip"]
    port = request.form["port"]
    location = {
        "long": request.form["long"],
        "lat": request.form["lat"]
    }
    # Overwrites old entries
    clusters[ip] = {
        "port": port,
        "location": location
    }
    return response_object(f"Added cluster '{ip}:{port}'.")


@app.route('/deregister-cluster', methods=['DELETE'])
def deregister_cluster():
    ip = request.form["ip"]
    # Overwrites old entries
    try:
        del clusters[ip]
        return response_object(f"Deleted cluster ip '{ip}'.")
    except KeyError:
        return response_object(f"Cluster ip '{ip}' is already non-existent and cannot be deleted.", 409)

