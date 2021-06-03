import json
import random
from threading import Thread

import requests
import plotting
import sys

from node_rest import NodeRest


def node_is_in_segment(location, min_location, max_location, number_of_segments, segment):
    length = max_location - min_location
    column_width = length / number_of_segments
    for segment_to_check in range(1, number_of_segments + 1):
        if column_width * segment_to_check + min_location >= location:
            return segment_to_check == segment


def node_is_in_column(longitude, min_longitude, max_longitude, number_of_columns, column):
    return node_is_in_segment(longitude, min_longitude, max_longitude, number_of_columns, column)


def node_is_in_row(latitude, min_latitude, max_latitude, number_of_rows, row):
    return node_is_in_segment(latitude, min_latitude, max_latitude, number_of_rows, row)

# starts rest APIs on given ports
from_port = 8890
number_of_nodes = 100

min_latitude = -90.0
max_latitude = 90.0
min_longitude = -180.0
max_longitude = 180.0
max_number_of_groups = 13

node_ip_port_id_group_list = []
threads = []

# create nodes
for port in range(from_port, from_port + number_of_nodes):
    node_rest = NodeRest("127.0.0.1", port)
    thread = Thread(target=node_rest.run)
    thread.start()
    threads.append(thread)
    node_ip_port_id_group_list.append({
        "ip": "127.0.0.1",
        "port": port
    })

# initialize nodes
for node_data in node_ip_port_id_group_list:
    init_data = scores_request_json = json.dumps({
        "cpu_power": 100,
        "storage_byte": 10000000000,
        "ram_byte": 500000000,
        "latitude": random.uniform(min_latitude, max_latitude),
        "longitude": random.uniform(min_longitude, max_longitude)
    })
    ip = node_data["ip"]
    port = node_data["port"]
    requests.post(f"http://{ip}:{port}/init", data=init_data)
    id = requests.get(f"http://{ip}:{port}/node_id").text
    node_data["id"] = id

# set peers for all nodes
for node_data in node_ip_port_id_group_list:
    ip = node_data["ip"]
    port = node_data["port"]
    peers_data = json.dumps(node_ip_port_id_group_list)
    requests.post(f"http://{ip}:{port}/set_peers", data=peers_data)

# group nodes
height = max_latitude - min_latitude
width = max_longitude - min_longitude
width_height_ratio = width / height
number_of_rows = 1
number_of_groups = None

while (True):
    new_number_of_groups = number_of_rows ** 2 + int((number_of_rows ** 2) * (width_height_ratio - 1))
    if new_number_of_groups <= max_number_of_groups:
        number_of_groups = new_number_of_groups
        number_of_rows += 1
    else:
        number_of_rows -= 1
        break

if number_of_groups is None:
    raise RuntimeError("Increase max number of groups.")

number_of_columns = int(number_of_groups / number_of_rows)
print(f"{number_of_rows} * {number_of_columns} = {number_of_groups}")

for node_data in node_ip_port_id_group_list:
    ip = node_data["ip"]
    port = node_data["port"]
    info = requests.get(f"http://{ip}:{port}/info").json()

    found_group = False
    for row in range(1, number_of_rows + 1):
        for col in range(1, number_of_columns + 1):
            is_in_column = node_is_in_column(info["location"]["longitude"], min_longitude, max_longitude, number_of_columns, col)
            is_in_row = node_is_in_row(info["location"]["latitude"], min_latitude, max_latitude, number_of_rows, row)
            if is_in_column and is_in_row:
                found_group = True
                node_data["group"] = (row, col)
                break
        if found_group:
            break
    print(node_data["group"])


# plot nodes
node_info_list = []
for node_data in node_ip_port_id_group_list:
    ip = node_data["ip"]
    port = node_data["port"]
    info = requests.get(f"http://{ip}:{port}/info").json()
    info["group"] = node_data["group"]
    node_info_list.append(info)
plotting.plot_nodes(node_info_list, (min_longitude, max_longitude), (min_latitude, max_latitude), number_of_rows, number_of_columns)
