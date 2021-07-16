import requests
import json
import asyncio
from node_data import leader_name, leader_ip, leader_secret, group_nodes


def delete_functions(name, ip, secret):
    functions = list(map(lambda function_data: function_data["name"], json.loads(requests.get(f"http://admin:{secret}@{ip}:8080/system/functions").content)))
    for function in functions:
        print(f"Deleting {function}@{name}|{ip}")
        url = f"http://admin:{secret}@{ip}:8080/system/functions"
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "functionName": function
        })
        requests.request("DELETE", url, headers=headers, data=payload)


for group_node in group_nodes():
    name = group_node["name"]
    ip = group_node["ip"]
    secret = group_node["secret"]
    delete_functions(name, ip, secret)
print("done")

# TODO remove data from databases (only that that no longer makes sense)