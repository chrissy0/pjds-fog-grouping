# V1.4 2021.07.19 18:22

import requests
import json
import os

wrapper_port = 5000
faasd_port = 8080


def get_external_ip():
    try:
        return os.environ['externalIp']
    except:
        raise RuntimeError("Error while retrieving external IP from environment variable in group member. Make sure it was set during function deployment.")


def get_function_ip(external_ip, function_name):
    error_msg = f"Could not retrieve address of function {function_name} from external address {external_ip}:{wrapper_port}."
    try:
        response = requests.post(f"http://{external_ip}:{wrapper_port}/get-address", data=function_name)
        if response.status_code != 200:
            raise RuntimeError
        return response.content.decode("utf-8")
    except:
        raise RuntimeError(error_msg)


def __call_fn(function_ip, function_name, data, kubernetes_mode=False):

    if kubernetes_mode:
        response = requests.get(f"http://gateway.openfaas:{faasd_port}/function/{function_name}", data=data)
        return response.content.decode("utf-8")

    for i in range(3):
        try:
            response = requests.get(f"http://{function_ip}:{faasd_port}/function/{function_name}", data=data)
        except:
            continue
        if response.status_code != 200:
            continue
        return response.content.decode("utf-8")
    raise RuntimeError(f"Next function {function_name} could not be called on {function_ip}.")


def __get_leader_address(external_ip):
    response = requests.get(f"http://{external_ip}:{wrapper_port}/get-leader-address")
    if response.status_code != 200:
        raise RuntimeError(f"Could not get leader address on {external_ip}.")
    return response



def __get_alternative_function_ip_from_leader(external_ip, function_name, failed_node_ip):
    response_leader_ip = __get_leader_address(external_ip)
    if response_leader_ip.status_code != 200:
        raise RuntimeError(f"Could not get leader address on node {external_ip}.")
    leader_ip = response_leader_ip.content.decode("utf-8")
    data = json.dumps({
        "requester": external_ip,
        "function": function_name,
        "address": failed_node_ip
    })
    response_alternative_ip = requests.post(f"http://{leader_ip}:{faasd_port}/function/find-alternatives", data=data)
    if response_alternative_ip.status_code != 200:
        raise RuntimeError(f"Could not get alternative node for function {function_name} from leader @{leader_ip}. Status Code: {response_alternative_ip.status_code}")
    return response_alternative_ip.content.decode("utf-8").strip()


def call_fn(function_name, data):
    kubernetes_mode = os.environ.get('kubernetesMode', False) == "True"

    if kubernetes_mode:
        return __call_fn(None, function_name, data, kubernetes_mode=True)

    external_ip = get_external_ip()
    function_ip = get_function_ip(external_ip, function_name)

    try:
        response = __call_fn(function_ip, function_name, data)
        return response
    except RuntimeError:
        alternative_function_ip = __get_alternative_function_ip_from_leader(external_ip, function_name, function_ip)
        try:
            response = __call_fn(alternative_function_ip, function_name, data)
            return response
        except RuntimeError:
            raise RuntimeError(f"Next function {function_name} could not be called on {function_ip}, even though alternative node ip {alternative_function_ip} was requested.")
