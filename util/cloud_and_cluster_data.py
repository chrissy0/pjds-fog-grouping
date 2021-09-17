cloud = {
    "ip": "34.141.21.222"
}

cluster_list = [
    {
        "name": "pjds-cluster-1",
        "ip": "34.142.37.134",  # kubectl get -n openfaas svc/gateway-external
        "secret": "70B2O763QM6NMG06F3nZFUcyc",  # echo $(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
        "lat": "52.3454",
        "lon": "13.645"
    },
    # {
    #     "name": "pjds-cluster-2",
    #     "ip": "34.142.126.102",
    #     "secret": "N7SDXP7GUAh20665S0rpE61Ah",
    #     "lat": "40.32444223",
    #     "lon": "16.87498"
    # },
]


def get_cloud():
    return cloud


def get_clusters():
    return cluster_list
