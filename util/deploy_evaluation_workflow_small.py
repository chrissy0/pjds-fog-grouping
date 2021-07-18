import json

import requests
from node_data import leader_ip


def deploy_evaluation_workflow(replicas=1, deployment_mode="grouped", group_size=1, log=False):
    request = json.dumps({
        "name": "evaluation-function-11",
        "registry": "pjdsgrouping/evaluation-function-11",
        "calls": [
            {
                "name": "evaluation-function-12",
                "registry": "pjdsgrouping/evaluation-function-12",
                "calls": []
            }
        ],
        "replicas": str(replicas),
        "deployment-mode": deployment_mode,
        "group-size": str(group_size)
    })

    response = requests.get(f"http://{leader_ip()}:8080/function/deploy-workflow", data=request)
    if log:
        print(f"Deploy evaluation workflow: {response.content.decode('utf-8')}")


# sudo faas-cli build -f evaluation-function-01.yml;sudo faas-cli build -f evaluation-function-02.yml;sudo faas-cli build -f evaluation-function-03.yml;sudo faas-cli build -f evaluation-function-04.yml;sudo faas-cli build -f evaluation-function-05.yml;sudo faas-cli build -f evaluation-function-06.yml;sudo faas-cli build -f evaluation-function-07.yml;sudo faas-cli build -f evaluation-function-08.yml;sudo faas-cli build -f evaluation-function-09.yml;sudo faas-cli build -f evaluation-function-10.yml;sudo faas-cli build -f evaluation-function-11.yml;sudo faas-cli build -f evaluation-function-12.yml;sudo faas-cli push -f evaluation-function-01.yml;sudo faas-cli push -f evaluation-function-02.yml;sudo faas-cli push -f evaluation-function-03.yml;sudo faas-cli push -f evaluation-function-04.yml;sudo faas-cli push -f evaluation-function-05.yml;sudo faas-cli push -f evaluation-function-06.yml;sudo faas-cli push -f evaluation-function-07.yml;sudo faas-cli push -f evaluation-function-08.yml;sudo faas-cli push -f evaluation-function-09.yml;sudo faas-cli push -f evaluation-function-10.yml;sudo faas-cli push -f evaluation-function-11.yml;sudo faas-cli push -f evaluation-function-12.yml


