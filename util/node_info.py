import requests
import json
from node_data import leader_name, leader_ip, leader_secret, group_nodes


def get_functions_on_node_string(name, ip, secret):
    string = ""
    functions = list(map(lambda function_data: function_data["name"], json.loads(requests.get(f"http://admin:{secret}@{ip}:8080/system/functions").content)))
    string += f"{name}@{ip} - {functions}\n"
    return string


def print_functions_on_node(name, ip, secret):
    print(get_functions_on_node_string(name, ip, secret))


def get_deployment_string():
    string = ""
    grouping_table = requests.get(f"http://{leader_ip()}:5000/get-all-nodes").content.decode("utf-8").split(",")
    for entry in grouping_table:
        # print(entry)
        string += entry + "\n"

    string += "\n"

    string += get_functions_on_node_string(f"{leader_name()} (leader)", leader_ip(), leader_secret())
    for group_node in group_nodes():
        name = group_node["name"] + "         "
        ip = group_node["ip"]
        secret = group_node["secret"]
        string += get_functions_on_node_string(name, ip, secret)

    return string


def print_node_info():
    print(get_deployment_string())
