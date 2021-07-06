# V1.2 2021.07.06 20:19

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


def __call_fn(function_ip, function_name, data):
    error_msg = f"Could not access function {function_name} at {function_ip}:{faasd_port}."
    # try:
    response = requests.get(f"http://{function_ip}:{faasd_port}/function/{function_name}", data=data)
    # if response.status_code != 200:
    #     raise RuntimeError(error_msg)
    return response.content.decode("utf-8")
    # except e:
    #     raise RuntimeError(error_msg, e)


def call_fn(function_name, data):
    external_ip = get_external_ip()
    function_ip = get_function_ip(external_ip, function_name)
    # TODO uncomment when there are dummy functions
    # TODO try calling multiple times, then request alternative from leader if necessary
    response = __call_fn(function_ip, function_name, data)
    return response

