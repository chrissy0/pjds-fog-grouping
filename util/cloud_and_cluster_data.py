cloud = {
    "ip": "34.141.127.189"
}

cluster_list = [
    {
        "name": "pjds-cluster-1",
        "openfaas_ip": "35.246.29.50",  # kubectl get -n openfaas svc/gateway-external
        "kubectl_pod_ip": "10.3.241.129",  # kubectl get service kubectl-service --output yaml | grep clusterIP:
        "cluster_ip": "35.189.80.227",  # kubectl get svc
        "secret": "F5sV631qQJCSeKSTY22oD5840",  # echo $(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
        "lat": "52.3454",
        "lon": "13.645",
        "cluster_name": "pjds-cluster-1",
        "zone": "europe-west2-c",
    },
    # {
    #     "name": "pjds-cluster-2",
    #     "openfaas_ip": "34.89.91.102",
    #     "kubectl_pod_ip": "10.115.240.230",
    #     "cluster_ip": "34.142.37.203",
    #     "secret": "guD0459ZLc2dpym4xL7Sh7O47",
    #     "lat": "40.32444223",
    #     "lon": "16.87498",
    #     "cluster_name": "abc",
    #     "zone": "def",
    # },
]


def get_cloud():
    return cloud


def get_clusters():
    return cluster_list
