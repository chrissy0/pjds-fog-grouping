import json
import random
from threading import Thread

import requests
import plotting

from node_rest import NodeRest

# starts rest APIs on given ports
from_port = 8890
number_of_nodes = 100

node_ip_port_id_list = []

# create nodes
for port in range(from_port, from_port + number_of_nodes):
    node_rest = NodeRest("127.0.0.1", port)
    thread = Thread(target=node_rest.run)
    thread.start()
    node_ip_port_id_list.append({
        "ip": "127.0.0.1",
        "port": port
    })

# initialize nodes
for node_data in node_ip_port_id_list:
    init_data = scores_request_json = json.dumps({
        "cpu_power": 100,
        "storage_byte": 10000000000,
        "ram_byte": 500000000,
        "latitude": random.uniform(-90.0, 90.0),
        "longitude": random.uniform(-180.0, 180.0)
    })
    ip = node_data["ip"]
    port = node_data["port"]
    requests.post(f"http://{ip}:{port}/init", data=init_data)
    id = requests.get(f"http://{ip}:{port}/node_id").text
    node_data["id"] = id

# set peers for all nodes
for node_data in node_ip_port_id_list:
    ip = node_data["ip"]
    port = node_data["port"]
    peers_data = json.dumps(node_ip_port_id_list)
    requests.post(f"http://{ip}:{port}/set_peers", data=peers_data)


# plot nodes
node_info_list = []
for node_data in node_ip_port_id_list:
    ip = node_data["ip"]
    port = node_data["port"]
    info = requests.get(f"http://{ip}:{port}/info").json()
    node_info_list.append(info)
plotting.plot_nodes(node_info_list)
