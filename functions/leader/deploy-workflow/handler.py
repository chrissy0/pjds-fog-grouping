import requests
import json
import os
import sys
from member_utility import get_external_ip

port = "5000"

def handle(req):
    body = json.loads(req)
    workflow = body["workflow"]
    functions = body["functions"]

    try:
        ip = get_external_ip()
    except:
        return json.dumps({
            "status-code": 500,
            "message": "Error while retrieving external IP from environment variable in group member. Make sure it was set during function deployment."
        })

    # Get Group members:
    res = requests.get(f"http://{ip}:{port}/get-all-nodes")
    if res.status_code != 200:
        return json.dumps({
            "status-code": res.status_code,
            "message": f"There was an error while retrieving group members for the leader with {ip}"
        })

    nodes = res.text.split(",")

    # TODO: Insert Load Analysis, get nodes ordered by available CPU/RAM

    # TODO: workflow

    # function-deployment
    for i, (func, rep) in enumerate(functions.items()):

        node_ip = nodes[i-1].split()[0]
        node_secret = nodes[i-1].split()[1]

        node_address = f"http://admin:{node_secret}@{node_ip}:8080"
        url = node_address + "/system/functions"

        headers = {
            'Content-Type': 'application/json'
        }

        # First delete function if already exists
        payload = json.dumps({
            "functionName": func
        })
        response = requests.request("DELETE", url, headers=headers, data=payload)
        if response.status_code != 200 and response.status_code != 404:
            return json.dumps({
                "status-code": res.status_code,
                "message": f"Problem with deletion of {func}",
                "error-message": response.text
            })

        # Deploy Function
        payload = json.dumps({
            "service": func,
            "network": "func_functions",
            "image": rep,
            "readOnlyRootFilesystem": True,
            "envVars": {
                "externalIp": node_ip
            }
        })

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            return json.dumps({
                "status-code": res.status_code,
                "message": f"Could not deploy function {func}",
                "error-message": response.text
            })

        # Store Function in SQLite
        res = requests.post(f"http://{ip}:{port}/add-fn", data=f"{func},{node_address}")
        if res.status_code != 200:
            return json.dumps({
                "status-code": res.status_code,
                "message": f"Could not store function {func} in database"
            })

        # Save information about next function:
        next_node = nodes[i-1].split()[0]
        res = requests.post(f"http://{node_ip}:{port}/set-address", data=f"{func},{next_node}")
        if res.status_code != 200:
            return json.dumps({
                "status-code": res.status_code,
                "message": f"Address {next_node} for function {func} could not be set on node at {node_ip}:{port}."
            })


    return "Deployed new workflow"
