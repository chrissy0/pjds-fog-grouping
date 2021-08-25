import requests
import json
import os
import sys
from member_utility import get_external_ip

port = "5000"


def handle(req):
    try:
        ip = get_external_ip()
    except:
        return json.dumps({
            "status-code": 500,
            "message": f"Error while retrieving external IP from environment variable in group member. Make sure it was set during function deployment."
        })

    payload = json.loads(req)

    function_name = payload["function_name"]
    address = payload["address"]

    try:
        response = requests.post(f"http://{ip}:{port}/set-address", data=f"{function_name},{address}")
    except:
        return json.dumps({
            "status-code": 500,
            "message": f"Node at {ip}:{port} could not be reached."
        })

    if response.status_code != 200:
        return json.dumps({
            "status-code": response.status_code,
            "message": f"Address {address} for function {function_name} could not be set on node at {ip}:{port}. Please try again later."
        })

    return json.dumps({
        "status-code": response.status_code
    })
