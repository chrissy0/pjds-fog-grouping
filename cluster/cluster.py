import json
from datetime import datetime
from timeit import default_timer as timer
import numpy as np

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask import jsonify
from flask import request

log = []

cloud_ip = None
cluster_external_ip = None
kubectl_pod_internal_ip = None
openfaas_ip = None
openfaas_secret = None
max_avg_cpu_usage = 0  # TODO change
rebalance_locked = False
registered = False
lat = None
lon = None
cluster_name = None
cluster_zone = None


def response_object(message=None, code=200):
    res = {}
    if message:
        add_to_log(message)
        res["message"] = message
    return res, code


def add_to_log(message, do_print=True):
    global log
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    log.append({
        "timestamp": timestamp,
        "message": message
    })
    if do_print:
        print(f"{timestamp} {message}")


def rebalance_resources():
    if rebalance_locked:
        return
    global registered
    if not registered:
        if cloud_ip is None or cluster_external_ip is None or kubectl_pod_internal_ip is None or lat is None or lon is None or openfaas_ip is None or openfaas_secret is None or cluster_name is None or cluster_zone is None:
            return
        data = {
            "ip": cluster_external_ip,
            "port": 5000,
            "openfaas_ip": openfaas_ip,
            "openfaas_secret": openfaas_secret,
            "lat": lat,
            "lon": lon
        }
        response = requests.post(f"http://{cloud_ip}:5000/register-cluster", data=data)
        if response.status_code == 200:
            registered = True
        else:
            return

    data = {
        "cluster": cluster_name,
        "zone": cluster_zone
    }
    response = requests.post(f"http://{kubectl_pod_internal_ip}:5001/set-config", data=data)
    if response.status_code != 200:
        return response_object(f"Could not set kubectl config.", 409)

    response = requests.get(f"http://{kubectl_pod_internal_ip}:5001/get-node-info")
    if response.status_code != 200:
        return response_object(f"Could not get node info from kubectl pod.", 409)
    cluster_node_info = json.loads(response.text)["node_info"]
    if len(cluster_node_info) == 0:
        # TODO more stuff to do here?
        return
    add_to_log(f"Got cluster node info: {cluster_node_info}")
    avg_cpu_usage = np.average(list(map(lambda x: float(x["cpu_percent"][:-1]), cluster_node_info)))
    if not (avg_cpu_usage > max_avg_cpu_usage):
        return

    add_to_log(f"current average node: {avg_cpu_usage}%")

    # get suggestions from cloud
    data = {
        "ip": cluster_external_ip,
        "limit": 10
    }
    response = requests.post(f"http://{cloud_ip}:5000/cluster-suggestions", data=data)
    if response.status_code != 200:
        add_to_log(
            f"Could not get nearby cluster suggestions for {cluster_external_ip}. Is the cluster registered in the cloud?")
    add_to_log(response.text)
    nearby_clusters = json.loads(response.text)["closest_clusters"]

    # get latency to clusters
    for nearby_cluster in nearby_clusters:
        ip = nearby_cluster["ip"]
        add_to_log(ip)
        for i in range(5):
            # measuring latency
            start_time = timer()
            response = requests.get(f"http://{ip}:5000/ping")
            end_time = timer()
            if response.status_code != 200:
                # TODO unexpected response, handle
                pass
            roundtrip_latency = end_time - start_time
            # keeping lowest measured latency
            if "latency" not in nearby_cluster or nearby_cluster["latency"] > roundtrip_latency:
                nearby_cluster["latency"] = roundtrip_latency

    nearby_clusters_sorted_by_latency = sorted(nearby_clusters, key=lambda k: k['latency'])
    add_to_log(nearby_clusters_sorted_by_latency)

    for cluster in nearby_clusters_sorted_by_latency:
        response = requests.get(f"http://{cluster['ip']}:5000/request-node-exchange")
        add_to_log(response.text)
        if response.status_code != 200:
            add_to_log(f"Could not agree on exchanging nodes with node @{cluster['ip']}")
            continue
        add_to_log(f"Adding new node, while {cluster['ip']} shuts down a node.")
        # TODO add new node now
        # TODO don't ask for new nodes again before new node is fully added
        return


sched = BackgroundScheduler(daemon=True)
sched.add_job(rebalance_resources, 'interval', seconds=5)  # TODO longer interval
sched.start()

app = Flask(__name__)


@app.route('/init-cluster', methods=['POST'])
def init_cluster():
    global cloud_ip, cluster_external_ip, kubectl_pod_internal_ip, openfaas_ip, openfaas_secret, lat, lon, cluster_name, cluster_zone
    cloud_ip = request.form["cloud_ip"]
    cluster_external_ip = request.form["cluster_external_ip"]
    kubectl_pod_internal_ip = request.form["kubectl_pod_internal_ip"]
    openfaas_ip = request.form["openfaas_ip"]
    openfaas_secret = request.form["openfaas_secret"]
    lat = request.form["lat"]
    lon = request.form["lon"]
    cluster_name = request.form["cluster_name"]
    cluster_zone = request.form["cluster_zone"]
    return response_object(f"Cluster was initialized.")


@app.route('/get-log', methods=['GET'])
def get_error_log():
    global log
    return jsonify(results=log)


@app.route('/request-node-exchange', methods=['GET'])
def request_node():
    if rebalance_locked:
        return response_object("Rebalancing is currently disabled for this cluster.", 409)
    global kubectl_pod_internal_ip
    if kubectl_pod_internal_ip is None:
        return response_object("kubectl_pod_internal_ip was not set.", 409)
    response = requests.get(f"http://{kubectl_pod_internal_ip}:5001/get-node-info")
    if response.status_code != 200:
        return response_object(f"Could not get node info from kubectl pod.", 409)
    cluster_node_info = json.loads(response.text)["node_info"]
    if len(cluster_node_info) == 1:
        return response_object(f"Cluster is already of size 1, cannot provide another node.", 409)
    avg_cpu_usage_after_shutting_down_another_node = sum(list(map(lambda x: float(x["cpu_percent"][:-1]), cluster_node_info))) / (len(cluster_node_info) - 1)
    if avg_cpu_usage_after_shutting_down_another_node > max_avg_cpu_usage:
        return response_object(f"Average CPU usage after removing one node exceeds {max_avg_cpu_usage}% ({avg_cpu_usage_after_shutting_down_another_node}%), thus no nodes can be offered.", 409)
    # TODO shutdown node
    return response_object("Node will be shutdown.", 200)



@app.route('/debug-request', methods=['POST'])
def debug_request():
    url = request.form["url"]
    try:
        data = request.form["data"]
    except:
        data = None
    response = requests.get(url, data=data)
    return f"Resp:\n{response.text}"


@app.route('/ping', methods=['GET'])
def ping_pong():
    return "pong"


# Returning exceptions
@app.errorhandler(Exception)
def exception_handler(error):
    return f"Error occurred: {repr(error)}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
