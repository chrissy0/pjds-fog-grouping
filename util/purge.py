import json

import requests
from node_data import leader_name, leader_ip, leader_secret, group_nodes


def empty_tables(ip):
    requests.post(f"http://{ip}:5000/empty-all-tables")


def delete_functions(name, ip, secret, log=False):
    while True:
        functions = list(map(lambda function_data: function_data["name"],
                             json.loads(requests.get(f"http://admin:{secret}@{ip}:8080/system/functions").content)))
        if len(functions) == 0:
            if log:
                print(f"Purged all functions on {name}, exiting function.")
            return
        for function in functions:
            if log:
                print(f"Deleting {function}@{name}|{ip}")
            url = f"http://admin:{secret}@{ip}:8080/system/functions"
            headers = {
                'Content-Type': 'application/json'
            }
            payload = json.dumps({
                "functionName": function
            })
            requests.request("DELETE", url, headers=headers, data=payload)


def delete_leader_functions(log=False):
    if log:
        print(f"Deleting leader functions ({leader_name()}@{leader_ip()})")
    delete_functions(leader_name(), leader_ip(), leader_secret())


def delete_all_group_functions(log=False):
    for group_node in group_nodes():
        name = group_node["name"]
        ip = group_node["ip"]
        secret = group_node["secret"]
        if log:
            print(f"Deleting group functions ({name}@{ip})")
        delete_functions(name, ip, secret)


def delete_all_functions(log=False):
    if log:
        print("Deleting all functions")
    delete_leader_functions(log)
    delete_all_group_functions(log)


def empty_leader_tables(log=False):
    if log:
        print(f"Emptying leader tables ({leader_name()}@{leader_ip()})")
    empty_tables(leader_ip())


def empty_all_group_tables(log=False):
    for group_node in group_nodes():
        name = group_node["name"]
        ip = group_node["ip"]
        if log:
            print(f"Emptying group member tables ({name}@{ip})")
        empty_tables(ip)


def empty_all_tables(log=False):
    if log:
        print("Emptying all tables")
    empty_leader_tables(log)
    empty_all_group_tables(log)


def purge_leader(log=False):
    if log:
        print("Purging leader")
    empty_leader_tables(log)
    delete_leader_functions(log)


def purge_group_members(log=False):
    if log:
        print("Purging group members")
    empty_all_group_tables(log)
    delete_all_group_functions(log)


def purge(log=False):
    if log:
        print("Purging everything")
    purge_leader(log)
    purge_group_members(log)


if __name__ == "__main__":
    purge(log=True)
