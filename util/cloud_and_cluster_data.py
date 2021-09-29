cloud = {
    "ip": "34.141.127.189"
}


cluster_list = [
    {
        "name": "<placeholder>",
        "openfaas_ip": "<placeholder>",  # kubectl get -n openfaas svc/gateway-external
        "kubectl_pod_ip": "<placeholder>",  # kubectl get service kubectl-gcloud-service --output yaml | grep clusterIP:
        "cluster_ip": "<placeholder>",  # kubectl get svc
        "secret": "<placeholder>",  # echo $(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
        "lat": "<placeholder>",
        "lon": "<placeholder>",
        "cluster_name": "<placeholder>",
        "zone": "<placeholder>",
    },
    {
        "name": "<placeholder>",
        "openfaas_ip": "<placeholder>",  # kubectl get -n openfaas svc/gateway-external
        "kubectl_pod_ip": "<placeholder>",  # kubectl get service kubectl-gcloud-service --output yaml | grep clusterIP:
        "cluster_ip": "<placeholder>",  # kubectl get svc
        "secret": "<placeholder>",  # echo $(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
        "lat": "<placeholder>",
        "lon": "<placeholder>",
        "cluster_name": "<placeholder>",
        "zone": "<placeholder>",
    },
]


def get_cloud():
    return cloud


def get_clusters():
    return cluster_list
