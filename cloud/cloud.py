from flask import Flask
from flask import request

app = Flask(__name__)


leaders = {}


def response_object(message=None, code=200):
    res = {"response": leaders}
    if message:
        res["message"] = message
    return res, code


@app.route('/register-leader', methods=['POST'])
def register_leader():
    ip = request.form["ip"]
    port = request.form["port"]
    # Overwrites old entries
    leaders[ip] = {
        "port": port
    }
    return response_object(f"Added leader '{ip}:{port}'.")


@app.route('/deregister-leader', methods=['DELETE'])
def deregister_leader():
    ip = request.form["ip"]
    # Overwrites old entries
    try:
        del leaders[ip]
        return response_object(f"Deleted leader ip '{ip}'.")
    except KeyError:
        return response_object(f"Leader ip '{ip}' is already non-existent and cannot be deleted.", 409)

