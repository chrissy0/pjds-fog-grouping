import json
import threading
from timeit import default_timer as timer

import requests
from deploy_evaluation_workflow import deploy_evaluation_workflow
from node_data import group_nodes
from node_info import get_deployment_string
from purge import purge
from setup_leader import setup_leader


def get_ip_of_fn(fn_name):
    for group_node in group_nodes():
        ip = group_node["ip"]
        secret = group_node["secret"]
        functions = list(map(lambda function_data: function_data["name"],
                             json.loads(requests.get(f"http://admin:{secret}@{ip}:8080/system/functions").content)))
        for function in functions:
            if function == fn_name:
                return ip
    raise RuntimeError(f"Function {fn_name} not deployed anywhere. Cannot get IP.")


def call_fn(fn_name, data, log=False):
    ip = get_ip_of_fn(fn_name)
    response = requests.get(f"http://{ip}:8080/function/{fn_name}", data=json.dumps(data))
    if log:
        print(response.content.decode("utf-8"))
    return response.status_code == 200, response.content.decode("utf-8")


test_results = []

group_modes = ["random", "grouped", "random", "random", "random", "random"]
group_sizes_for_grouped = range(1, 5 + 1)
durations = [0, 0.1, 0.25, 0.5, 1, 2, 5, 10]
iterations = 5

purge(log=True)
setup_leader()
deploy_evaluation_workflow(1, "grouped", 1)
deployment_string = get_deployment_string()
print(deployment_string)

data = {
    "duration": 0,
    "log": []
}

response_times = []


def call_in_thread():
    print("in thread")
    start = timer()
    successful, response = call_fn("evaluation-function-01", data, log=True)
    end = timer()
    response_times.append(end - start)
    print(response_times)

threads = []

for i in range(10):
    th = threading.Thread(target=call_in_thread)
    threads.append(th)
    th.start()

for th in threads:
    th.join()
