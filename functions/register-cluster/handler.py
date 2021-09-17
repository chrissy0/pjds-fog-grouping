import requests
import os


def get_cloud_ip():
    return os.environ['cloudIp']


def get_cloud_port():
    return 5000


def get_cluster_ip():
    return os.environ['clusterIp']


def get_cluster_port():
    return 5000


def get_lat():
    return os.environ['lat']


def get_lon():
    return os.environ['lon']


def handle(req):
    # request cluster ip
    ip = get_cluster_ip()
    # request cluster port
    port = get_cluster_port()
    # request location
    lat = get_lat()
    lon = get_lon()
    data = {
        "ip": ip,
        "port": port,
        "lat": lat,
        "lon": lon
    }
    requests.post(f"http://{get_cloud_ip()}:{get_cloud_port()}/register-cluster", data=data)

# after changes, do: `sudo faas-cli build -f register-cluster.yml;sudo faas-cli push -f register-cluster.yml`