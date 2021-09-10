import json
import requests


cloud_ip = "34.141.21.222"
cluster_ip = "35.197.228.182"
lat = "50.3"
lon = "13.2"


function_name = "register-cluster"
registry_url = "pjdsgrouping/register-cluster:latest"


openfaas_gateway_ip = "35.197.228.182"
openfaas_gateway_port = "8080"
openfaas_secret = "oS79L001B60K6Z76MSwPFhhei"
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
