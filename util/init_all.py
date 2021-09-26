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

    cluster_name = cluster["cluster_name"]
    cluster_zone = cluster["zone"]


    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", f"http://{cluster_ip}:5000/init-cluster", headers=headers, data={
        "cloud_ip": cloud_ip,
        "cluster_external_ip": cluster_ip,
        "kubectl_pod_internal_ip": kubectl_pod_ip,
        "openfaas_ip": openfaas_ip,
        "openfaas_secret": openfaas_secret,
        "lat": lat,
        "lon": lon,
        "cluster_name": cluster_name,
        "cluster_zone": cluster_zone
    })
    print(f"Initializing cluster: {response}")



