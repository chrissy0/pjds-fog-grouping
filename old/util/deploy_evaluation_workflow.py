import json

import requests
from node_data import leader_ip


def deploy_evaluation_workflow(replicas=1, deployment_mode="grouped", group_size=1, log=False):
    request = json.dumps({
        "name": "evaluation-function-01",
        "registry": "pjdsgrouping/evaluation-function-01",
        "calls": [
            {
                "name": "evaluation-function-02",
                "registry": "pjdsgrouping/evaluation-function-02",
                "calls": [
                    {
                        "name": "evaluation-function-03",
                        "registry": "pjdsgrouping/evaluation-function-03",
                        "calls": [
                            {
                                "name": "evaluation-function-04",
                                "registry": "pjdsgrouping/evaluation-function-04",
                                "calls": [
                                    {
                                        "name": "evaluation-function-05",
                                        "registry": "pjdsgrouping/evaluation-function-05",
                                        "calls": [
                                            {
                                                "name": "evaluation-function-06",
                                                "registry": "pjdsgrouping/evaluation-function-06",
                                                "calls": [
                                                    {
                                                        "name": "evaluation-function-07",
                                                        "registry": "pjdsgrouping/evaluation-function-07"
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "name": "evaluation-function-08",
                                "registry": "pjdsgrouping/evaluation-function-08",
                                "calls": [
                                    {
                                        "name": "evaluation-function-09",
                                        "registry": "pjdsgrouping/evaluation-function-09",
                                        "calls": [
                                            {
                                                "name": "evaluation-function-10",
                                                "registry": "pjdsgrouping/evaluation-function-10"
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "name": "evaluation-function-11",
                "registry": "pjdsgrouping/evaluation-function-11",
                "calls": [
                    {
                        "name": "evaluation-function-12",
                        "registry": "pjdsgrouping/evaluation-function-12"
                    }
                ]
            }
        ],
        "replicas": str(replicas),
        "deployment-mode": deployment_mode,
        "group-size": str(group_size)
    })

    response = requests.get(f"http://{leader_ip()}:8080/function/deploy-workflow", data=request)
    if log:
        print(f"Deploy evaluation workflow: {response.content.decode('utf-8')}")


if __name__ == "__main__":
    deploy_evaluation_workflow()

# sudo faas-cli build -f evaluation-function-01.yml;sudo faas-cli build -f evaluation-function-02.yml;sudo faas-cli build -f evaluation-function-03.yml;sudo faas-cli build -f evaluation-function-04.yml;sudo faas-cli build -f evaluation-function-05.yml;sudo faas-cli build -f evaluation-function-06.yml;sudo faas-cli build -f evaluation-function-07.yml;sudo faas-cli build -f evaluation-function-08.yml;sudo faas-cli build -f evaluation-function-09.yml;sudo faas-cli build -f evaluation-function-10.yml;sudo faas-cli build -f evaluation-function-11.yml;sudo faas-cli build -f evaluation-function-12.yml;sudo faas-cli push -f evaluation-function-01.yml;sudo faas-cli push -f evaluation-function-02.yml;sudo faas-cli push -f evaluation-function-03.yml;sudo faas-cli push -f evaluation-function-04.yml;sudo faas-cli push -f evaluation-function-05.yml;sudo faas-cli push -f evaluation-function-06.yml;sudo faas-cli push -f evaluation-function-07.yml;sudo faas-cli push -f evaluation-function-08.yml;sudo faas-cli push -f evaluation-function-09.yml;sudo faas-cli push -f evaluation-function-10.yml;sudo faas-cli push -f evaluation-function-11.yml;sudo faas-cli push -f evaluation-function-12.yml
