cloud = {
    "ip": "34.141.127.189"
}


# TODO change to placeholder
cluster_list = [
    {
        "name": "pjds-cluster-1",
        "openfaas_ip": "35.246.29.50",  # kubectl get -n openfaas svc/gateway-external
        "kubectl_pod_ip": "10.3.242.117",  # kubectl get service kubectl-gcloud-service --output yaml | grep clusterIP:
        "cluster_ip": "35.189.80.227",  # kubectl get svc
        "secret": "F5sV631qQJCSeKSTY22oD5840",  # echo $(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
        "lat": "52.3454",
        "lon": "13.645",
        "cluster_name": "pjds-cluster-1",
        "zone": "europe-west2-c",
    },
    {
        "name": "pjds-cluster-2",
        "openfaas_ip": "34.105.201.225",
        "kubectl_pod_ip": "10.115.241.37",
        "cluster_ip": "34.142.80.184",
        "secret": "Hf9k493FIaBp40O97yyo2Xj7k",
        "lat": "40.32444223",
        "lon": "16.87498",
        "cluster_name": "pjds-cluster-2",
        "zone": "europe-west2-c",
    },
]


def get_cloud():
    return cloud


def get_clusters():
    return cluster_list
