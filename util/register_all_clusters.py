import json
import requests
from cloud_and_cluster_data import get_cloud
from cloud_and_cluster_data import get_clusters


cloud_ip = get_cloud()["ip"]

function_name = "register-cluster"
registry_url = "pjdsgrouping/register-cluster:latest"

for cluster in get_clusters():
    cluster_ip = cluster["ip"]
    lat = cluster["lat"]
    lon = cluster["lon"]
    
    openfaas_gateway_ip = cluster_ip
    openfaas_gateway_port = "8080"
    openfaas_secret = cluster["secret"]
    url = f"http://admin:{openfaas_secret}@{openfaas_gateway_ip}:{openfaas_gateway_port}/system/functions"
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Deploy Function
    payload = json.dumps({
        "service": function_name,
        "network": "func_functions",
        "image": registry_url,
        "readOnlyRootFilesystem": True,
        "envVars": {
            "cloudIp": cloud_ip,
            "clusterIp": cluster_ip,
            "lat": lat,
            "lon": lon
        }
    })
    
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
    if response.status_code != 202:
        response = requests.request("PUT", url, headers=headers, data=payload)
        print(response)
    if response.status_code != 202:
        # TODO handle
        print("Deployment not successful.")
    
    
    function_url = f"http://{openfaas_gateway_ip}:{openfaas_gateway_port}/function/{function_name}"
    response = requests.request("GET", function_url)
    print(response)
