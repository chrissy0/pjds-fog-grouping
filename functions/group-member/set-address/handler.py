import requests
import json
import os
import sys

ip = "127.0.0.1"
port = "5000"


def handle(req):
    payload = json.loads(req)

    function_name = payload["function_name"]
    address = payload["address"]

    response = requests.post(f"http://{ip}:{port}/set-address", data=f"{function_name},{address}")
    if response.status_code != 200:
        return json.dumps({
            "status-code": response.status_code,
            "message": "Address could not be set. Please try again later."
        })

    return json.dumps({
        "status-code": response.status_code
    })
