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

    nodes = res.text.split(",")

    # Turning "a->b->c" into [("a", "b"), ("b", "c"), ("c", None)]. The last element is needed so "c" is still deployed.
    function_dependencies = []
    functions_chain = workflow.split("->")
    for i in range(len(functions_chain) - 1):
        function_dependencies.append((functions_chain[i], functions_chain[i+1]))
    function_dependencies.append((functions_chain[-1], None))

    # TODO: Insert Load Analysis, get nodes ordered by available CPU/RAM

    # TODO: workflow


    for i, (source_func, target_func) in enumerate(function_dependencies):
        # Modulo % so we don't exceed number of nodes. Wraps around!
        source_node = nodes[i % len(nodes)]
        source_node_ip = source_node.split()[0]
        source_node_secret = source_node.split()[1]
        # Modulo % so we don't exceed number of nodes. Wraps around!
        target_node = nodes[(i+1) % len(nodes)]
        target_node_ip = target_node.split()[0]

        node_address = f"http://admin:{source_node_secret}@{source_node_ip}:8080"
        url = node_address + "/system/functions"

        headers = {
            'Content-Type': 'application/json'
        }

        # First delete function if already exists
        payload = json.dumps({
            "functionName": source_func
        })
        response = requests.request("DELETE", url, headers=headers, data=payload)
        if response.status_code != 200 and response.status_code != 404:
            return json.dumps({
                "status-code": res.status_code,
                "message": f"Problem with deletion of {func}",
                "error-message": response.text
            })

        # Deploy Function
        source_func_rep = functions[source_func]
        payload = json.dumps({
            "service": source_func,
            "network": "func_functions",
            "image": source_func_rep,
            "readOnlyRootFilesystem": True,
            "envVars": {
                "externalIp": source_node_ip
            }
        })

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            return json.dumps({
                "status-code": res.status_code,
                "message": f"Could not deploy function {source_func}",
                "error-message": response.text
            })

        # Store Function in SQLite
        res = requests.post(f"http://{external_ip}:{port}/add-fn", data=f"{source_func},{source_node_ip}")
        if res.status_code != 200:
            return json.dumps({
                "status-code": res.status_code,
                "message": f"Could not store function {source_func} in database"
            })

        # Save information about next function:
        if target_func is not None:
            res = requests.post(f"http://{source_node_ip}:{port}/set-address", data=f"{target_func},{target_node_ip}")
            if res.status_code != 200:
                return json.dumps({
                    "status-code": res.status_code,
                    "message": f"Address {target_node_ip} for function {target_func} could not be set on node at {source_node_ip}:{port}."
                })


    return "Deployed new workflow"

