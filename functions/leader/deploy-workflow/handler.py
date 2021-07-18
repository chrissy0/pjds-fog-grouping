import requests
import json
import os
import sys
import random
from member_utility import get_external_ip

port = "5000"

def handle(req):
    body = json.loads(req)

    try:
        replicas = int(body["replicas"])
    except:
        replicas = 2

    try:
        external_ip = get_external_ip()
    except:
        return json.dumps({
            "status-code": 500,
            "message": "Error while retrieving external IP from environment variable in group member. Make sure it was set during function deployment."
        })

    # Get Group members:
    res = requests.get(f"http://{external_ip}:{port}/get-all-nodes")
    if res.status_code != 200:
        return json.dumps({
            "status-code": res.status_code,
            "message": f"There was an error while retrieving group members for the leader with {external_ip}"
        })


    # Load Analysis, get nodes ordered by available CPU/RAM
    nodes = res.text.split(",")
    nodes = [node.split() for node in nodes]
    nodes = sorted(nodes, key=lambda x: (x[1], x[2]))

    # TODO: leave out nodes below certain threshold?

    # Deployment modes
    try:
        deployment_mode = body["deployment-mode"]
    except:
        deployment_mode = "default"


    try:
        group_size = int(body["group-size"])
    except:
        group_size = 1


    for i in range(replicas):
        deploy_function(deployment_mode, nodes, body, external_ip, i, None, group_size)



    return "Deployed new workflow"


def deploy_function(deployment_mode, nodes, body, external_ip, i, previous=None, grp_size=1, grp_i=0):
    try:
        name = body["name"]
    except:
        return json.dumps({
            "message": "Please state the name of your function"
        })

    try:
        registry = body["registry"]
    except:
        return json.dumps({
            "message": "Please state the link to the registry of your function"
        })

    try:
        calls = body["calls"]
    except:
        calls = None

    if deployment_mode == "random":
        node = random.choice(nodes)
    elif deployment_mode == "single-node":
        node = nodes[i]
    elif deployment_mode == "grouped":
        node = nodes[(grp_i - 1) % len(nodes)]
    else:
        node = nodes[i % len(nodes)]

    node_ip = node[0]
    node_secret = node[3]

    # Save Information about function on previous node
    if previous is not None:
        res = requests.post(f"http://{previous}:{port}/set-address", data=f"{name},{node_ip}")
        if res.status_code != 200:
            return json.dumps({
                "status-code": res.status_code,
                "message": f"Address {node_ip} for function {name} could not be set on node at {previous}:{port}."
            })


    node_address = f"http://admin:{node_secret}@{node_ip}:8080"
    url = node_address + "/system/functions"

    headers = {
        'Content-Type': 'application/json'
    }

    # Deploy Function
    payload = json.dumps({
        "service": name,
        "network": "func_functions",
        "image": registry,
        "readOnlyRootFilesystem": True,
        "envVars": {
            "externalIp": node_ip
        }
    })

    response = requests.request("POST", url, headers=headers, data=payload)
    # Use Put if function is already deployed to update
    if response.status_code == 400:
        response = requests.request("PUT", url, headers=headers, data=payload)

    if response.status_code != 200:
        return json.dumps({
            "status-code": response.status_code,
            "message": f"Could not deploy function {name}",
            "error-message": response.text
        })

    # Store Function in SQLite
    res = requests.post(f"http://{external_ip}:{port}/add-fn", data=f"{name},{node_ip}")
    if res.status_code != 200:
        return json.dumps({
            "status-code": res.status_code,
            "message": f"Could not store function {name} in database"
        })

    if calls is not None:
        for call in calls:
            if deployment_mode != "single-node":
                i += 1
            if i % grp_size == 0:
                grp_i += 1
            deploy_function(deployment_mode, nodes, call, external_ip, i, node_ip, grp_size, grp_i)
    else:
        return "Calls is empty"


    return "Finished Internal Call"