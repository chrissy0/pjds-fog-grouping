import requests
import json
from node_data import leader_ip, leader_secret, group_nodes

def setup_leader():
    # add nodes to leader
    for group_node in group_nodes():
        requests.post(f"http://{leader_ip()}:5000/add-node", f"{group_node['ip']},1,4,{group_node['secret']}")

    # deploying "deploy-workflow" function
    headers = {
            'Content-Type': 'application/json'
        }
    payload = json.dumps({
            "service": "deploy-workflow",
            "network": "func_functions",
            "image": "pjdsgrouping/deploy-workflow:latest",
            "readOnlyRootFilesystem": True,
            "envVars": {
                "externalIp": leader_ip()
            }
        })
    url = f"http://admin:{leader_secret()}@{leader_ip()}:8080/system/functions"
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 400:
        response = requests.request("PUT", url, headers=headers, data=payload)
    if response.status_code != 200:
        print("Couldn't deploy \"deploy-workflow\" function.")

    # TODO set leader IP on nodes