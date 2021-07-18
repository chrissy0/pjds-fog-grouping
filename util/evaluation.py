import json
from timeit import default_timer as timer
import requests
from deploy_evaluation_workflow_small import deploy_evaluation_workflow
from node_data import group_nodes
from node_info import get_deployment_string
from purge import purge
from setup_leader import setup_leader
import pickle
import datetime as dt


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


test_results = []

group_modes = ["grouped", "random"]
group_sizes = range(1, 2+1)
durations = [0, 0.25, 0.5, 1]
iterations = 10

for group_mode in group_modes:
    if group_mode != "grouped":
        group_sizes = [1]

    test_results.append({})
    test_results[-1]["group_mode"] = group_mode
    test_results[-1]["group_sizes"] = []

    for group_size in group_sizes:
        test_results[-1]["group_sizes"].append({})
        test_results[-1]["group_sizes"][-1]["group_size"] = group_size
        test_results[-1]["group_sizes"][-1]["durations"] = []

        purge()
        setup_leader()
        print(f"Deploying [mode: {group_mode}, group size: {group_size}]")
        deploy_evaluation_workflow(1, group_mode, group_size)

        test_results[-1]["group_sizes"][-1]["deployment"] = get_deployment_string()

        for duration in durations:
            test_results[-1]["group_sizes"][-1]["durations"].append({})
            test_results[-1]["group_sizes"][-1]["durations"][-1]["duration"] = duration
            test_results[-1]["group_sizes"][-1]["durations"][-1]["measurements"] = []

            print(f"Duration: {duration}")
            data = {
                "duration": duration,
                "log": []
            }
            for i in range(iterations):
                print(f"#{i+1}")
                start = timer()
                call_fn("evaluation-function-11", data)
                end = timer()
                print(end - start)
                test_results[-1]["group_sizes"][-1]["durations"][-1]["measurements"].append(end - start)

pickle.dump(test_results, open(f"test_results_{dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.p", "wb"))