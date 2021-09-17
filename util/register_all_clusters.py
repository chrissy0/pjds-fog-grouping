import json
import requests
from cloud_and_cluster_data import get_cloud
from cloud_and_cluster_data import get_clusters


cloud_ip = get_cloud()["ip"]

function_name = "register-cluster"
registry_url = "pjdsgrouping/register-cluster:latest"

for cluster in get_clusters():
    openfaas_ip = cluster["openfaas_ip"]
    lat = cluster["lat"]
    lon = cluster["lon"]
    
    openfaas_gateway_ip = openfaas_ip
    openfaas_gateway_port = "8080"
    openfaas_secret = cluster["secret"]

    cluster_ip = cluster["cluster_ip"]
    kubectl_pod_ip = cluster["kubectl_pod_ip"]

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
    print(f"Registering cluster in cloud: {response}")

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", f"http://{cluster_ip}:5000/set-cloud-ip", headers=headers, data={
        "ip": cloud_ip
    })
    print(f"Setting cloud ip: {response}")

    response = requests.request("POST", f"http://{cluster_ip}:5000/set-cluster-external-ip", headers=headers, data={
        "ip": cluster_ip
    })
    print(f"Setting cluster external ip: {response}")

    response = requests.request("POST", f"http://{cluster_ip}:5000/set-kubectl-pod-internal-ip", headers=headers, data={
        "ip": kubectl_pod_ip
    })
    print(f"Setting cluster external ip: {response}")


