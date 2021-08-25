import json
import os
import time
from datetime import datetime

from member_utility import call_fn
from member_utility import get_external_ip


def call_and_log(function_name, functions_to_call, init_messages, req):
    kubernetes_mode = os.environ.get('kubernetesMode', False) == "True"

    body = json.loads(req)
    duration_in_seconds = body["duration"]

    if init_messages:
        body["log"] = []

    if kubernetes_mode:
        body["log"].append(
            f"{datetime.now()}: {function_name} on Kubernetes stressing node for {duration_in_seconds}s.")
    else:
        body["log"].append(
            f"{datetime.now()}: {function_name} on {get_external_ip()} stressing node for {duration_in_seconds}s.")
    cpu_stress(duration_in_seconds)

    for function_to_call in functions_to_call:
        if kubernetes_mode:
            body["log"].append(f"{datetime.now()}: {function_name} on Kubernetes calling {function_to_call}.")
        else:
            body["log"].append(f"{datetime.now()}: {function_name} on {get_external_ip()} calling {function_to_call}.")
        req = json.dumps(body)
        ret = call_fn(function_to_call, req)
        body = json.loads(ret)

    if kubernetes_mode:
        body["log"].append(f"{datetime.now()}: {function_name} on Kubernetes done.")
    else:
        body["log"].append(f"{datetime.now()}: {function_name} on {get_external_ip()} done.")

    return json.dumps(body)


def cpu_stress(seconds):
    start = time.perf_counter()

    while True:
        # TODO find better way to produce load. Importing numpy produced error during compilation (bc. of base image? https://stackoverflow.com/questions/55032695/docker-build-for-numpy-pandas-giving-error)
        x = 52389756298372384569823756 / 328643428847562348975 * 2634856239452634

        current = time.perf_counter()
        if current - start >= seconds:
            break
