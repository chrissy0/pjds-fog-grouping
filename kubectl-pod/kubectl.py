import os
import sys

from flask import Flask
from flask import request

app = Flask(__name__)

GC_BIN = "./google-cloud-sdk/bin/gcloud"

CLUSTER = "cluster-victor"
ZONE = ""
NODESIZE_KEY = "currentNodeCount: "

def kubectl_top_nodes():
    response = os.popen("kubectl top nodes").read()

    nodes = []

    for line in response.splitlines()[1:]:
        line = line.split(" ")
        line = list(filter(None, line))
        name = line[0]
        cpu_cores = line[1]
        cpu_percent = line[2]
        memory_bytes = line[3]
        memory_percent = line[4]
        node_info = {
            "name": name,
            "cpu_cores": cpu_cores,
            "cpu_percent": cpu_percent,
            "memory_bytes": memory_bytes,
            "memory_percent": memory_percent,
        }
        nodes.append(node_info)

    return {
        "node_info": nodes,
        "message": "Could not retrieve node info" if len(response) == 0 else ""
    }

def drain_delete(node):
    node_group = node[:-4]
    _ = os.popen(f"kubectl drain {node} --ignore-daemonsets").read() #use read() to wait for execution
    _ = os.popen(f"{GC_BIN} compute instance-groups managed delete-instances {node_group}grp --instances={node} --zone {ZONE}").read()
    os.popen(f"{GC_BIN} compute instances delete {node} --zone {ZONE} -q")

def extract_nodepool_size(output):
    start = output.find(NODESIZE_KEY) + len(NODESIZE_KEY)
    end = start + 1
    while output[end].isnumeric():
        end = end + 1
    nodepool_size = int(output[start:end]) + 1
    return nodepool_size


@app.route('/set-config', methods=['POST'])
def set_config():
    global CLUSTER
    global ZONE
    req = request.json
    CLUSTER = req["cluster"]
    ZONE = req["zone"]
    os.popen(f"{GC_BIN} container clusters get-credentials {CLUSTER} --zone {ZONE}")
    return f"Cluster: {CLUSTER} and Zone: {ZONE} set"

@app.route('/get-node-info', methods=['GET'])
def get_node_info():
    return kubectl_top_nodes()

@app.route('/delete-node', methods=['POST'])
def delete_node():
    req = request.json
    node = req["node"]
    drain_delete(node)
    return "Node deleted"

@app.route('/add-node', methods=['GET'])
def add_node():
    output = os.popen(f"{GC_BIN} container node-pools list --cluster {CLUSTER}").read().split()
    node_pool_name = output[4] # Take the first node-pool (Assume we only use one per cluster anyway)
    output = os.popen(f"{GC_BIN} container clusters describe {CLUSTER} --zone {ZONE}").read()
    node_pool_size = extract_nodepool_size(output)
    os.popen(f"{GC_BIN} container clusters resize {CLUSTER} --node-pool {node_pool_name} --num-nodes {node_pool_size} --zone {ZONE} -q")
    return "Node added"


if __name__ == '__main__':
    if len(sys.argv) == 3:
        args = sys.argv
        CLUSTER = args[1]
        ZONE = args[2]
    app.run(host="0.0.0.0", port=5001)
