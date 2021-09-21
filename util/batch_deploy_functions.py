import json

import requests
from cloud_and_cluster_data import get_cloud
from cloud_and_cluster_data import get_clusters

cloud_ip = get_cloud()["ip"]

function_name = "ping-pong"
registry_url = "pjdsgrouping/ping-pong:latest"

for cluster in get_clusters():
    openfaas_ip = cluster["openfaas_ip"]
    lat = cluster["lat"]
    lon = cluster["lon"]

    openfaas_gateway_ip = openfaas_ip
    openfaas_gateway_port = "8080"
    openfaas_secret = cluster["secret"]

    cluster_ip = cluster["cluster_ip"]
    kubectl_pod_ip = cluster["kubectl_pod_ip"]

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", f"http://{cloud_ip}:5000/deploy-functions", headers=headers, data=json.dumps({
        "ip": cluster_ip,
        "functions": [
            {
                "name": "ping-pong",
                "registry_url": f"pjdsgrouping/ping-pong"
            },
            {
                "name": "ping-pong-pang",
                "registry_url": f"pjdsgrouping/ping-pong-pang"
            }
        ]
    }))
    print(f"Deploying functions: {response}")
    print(response.text)


    # testing deployment
    print("ping-pong")
    response = requests.request("GET", f"http://{openfaas_ip}:8080/function/ping-pong")
    print(response)
    print(response.text)
    print("ping-pong-pang")
    response = requests.request("GET", f"http://{openfaas_ip}:8080/function/ping-pong-pang")
    print(response)
    print(response.text)


