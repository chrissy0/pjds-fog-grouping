from apscheduler.schedulers.background import BackgroundScheduler

from flask import Flask
from flask import jsonify
from flask import request

from datetime import datetime
import requests
import json


error_log = []


cloud_ip = None
cluster_external_ip = None


def response_object(message=None, code=200):
    res = {}
    if message:
        res["message"] = message
    return res, code


def add_to_error_log(message, log=True):
    global error_log
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    error_log.append({
        "timestamp": timestamp,
        "message": message
    })
    if log:
        print(timestamp)


def rebalance_resources():
    print(f"cloud_ip: {cloud_ip}")
    print(f"cluster_external_ip: {cluster_external_ip}")
    if cloud_ip is None or cluster_external_ip is None:
        return

    # get suggestions from cloud
    data = {
        "ip": cluster_external_ip,
        "limit": 5
    }
    response = requests.post(f"http://{cloud_ip}:5000/cluster-suggestions", data=data)
    if response.status_code != 200:
        add_to_error_log(f"Could not get nearby cluster suggestions for {cluster_external_ip}. Is the cluster registered in the cloud?")
    nearby_clusters = json.loads(response.text)["closest_clusters"]

    # get latency to clusters
    # TODO setup and register 2 clusters, check actual latency (cluster_ip:8080, regardless of status code)
    print(nearby_clusters)


sched = BackgroundScheduler(daemon=True)
sched.add_job(rebalance_resources, 'interval', seconds=5)
sched.start()

app = Flask(__name__)


@app.route('/set-cloud-ip', methods=['POST'])
def set_cloud_ip():
    global cloud_ip
    cloud_ip = request.form["ip"]
    return response_object(f"Cloud ip was set to {cloud_ip}")


@app.route('/set-cluster-external-ip', methods=['POST'])
def set_cluster_external_ip():
    global cluster_external_ip
    cluster_external_ip = request.form["ip"]
    return response_object(f"Cluster external ip was set to {cluster_external_ip}")


@app.route('/get-error-log', methods=['GET'])
def get_error_log():
    global error_log
    return jsonify(results=error_log)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
