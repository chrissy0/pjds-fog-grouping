import json
from timeit import default_timer as timer
import requests
from deploy_evaluation_workflow import deploy_evaluation_workflow
from node_data import group_nodes
from node_info import get_deployment_string
from purge import purge
from setup_leader import setup_leader
import pickle
import datetime as dt
from evaluation_plotting import evaluate


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

group_modes = ["random", "grouped"]
group_sizes_for_grouped = range(1, 5+1)
durations = [0, 0.1, 0.25, 0.5, 1, 2, 5, 10]
iterations = 5

for group_mode in group_modes:
    group_sizes = group_sizes_for_grouped
    if group_mode != "grouped":
        group_sizes = [1]

    test_results.append({})
    test_results[-1]["group_mode"] = group_mode
    test_results[-1]["group_sizes"] = []

    for group_size in group_sizes:
        test_results[-1]["group_sizes"].append({})
        test_results[-1]["group_sizes"][-1]["group_size"] = group_size
        test_results[-1]["group_sizes"][-1]["durations"] = []

        purge(log=True)
        setup_leader()
        print(f"Deploying [mode: {group_mode}, group size: {group_size}]")
        deploy_evaluation_workflow(1, group_mode, group_size)

        deployment_string = get_deployment_string()
        print(deployment_string)
        test_results[-1]["group_sizes"][-1]["deployment"] = deployment_string

        for duration in durations:
            test_results[-1]["group_sizes"][-1]["durations"].append({})
            test_results[-1]["group_sizes"][-1]["durations"][-1]["duration"] = duration
            test_results[-1]["group_sizes"][-1]["durations"][-1]["measurements"] = []
            test_results[-1]["group_sizes"][-1]["durations"][-1]["non-200-response-on-iteration"] = []
            test_results[-1]["group_sizes"][-1]["durations"][-1]["responses"] = []

            print(f"Duration: {duration}")
            data = {
                "duration": duration,
                "log": []
            }
            for i in range(iterations):

                print(f"#{i+1}")
                start = timer()
                # TODO check more carefully if the call was successful. Returned True even though execution time limit was not set.
                successful, response = call_fn("evaluation-function-01", data, log=True)
                end = timer()
                print(end - start)
                test_results[-1]["group_sizes"][-1]["durations"][-1]["measurements"].append(end - start)
                if not successful:
                    test_results[-1]["group_sizes"][-1]["durations"][-1]["non-200-response-on-iteration"].append(i + 1)
                test_results[-1]["group_sizes"][-1]["durations"][-1]["responses"].append(response)
                pickle.dump(test_results,
                            open(f"test_results_{dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}_{group_mode}_{group_size}_{duration}_{i}.p", "wb"))
                evaluate(test_results)


pickle.dump(test_results, open(f"test_results_{dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}_done.p", "wb"))