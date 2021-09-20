import os

from flask import Flask
from flask import request

app = Flask(__name__)


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

def drain_node(node):
    os.popen(f"kubectl drain {node} --ignore-daemonsets")

@app.route('/get-node-info', methods=['GET'])
def get_node_info():
    return kubectl_top_nodes()

@app.route('/drain-node', methods=['POST'])
def remove_node():
    node = request.form("node")
    drain_node(node)
    # Initiate adding node here?

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
