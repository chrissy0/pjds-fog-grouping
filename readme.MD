<p align="center">
  <a href="" rel="noopener">
 <img src="https://i.imgur.com/NpIKJE4.png" alt="Project logo"></a>
</p>

---

<p align="center"><i>Making resources available where they're needed.</i></p>


## 📝 Table of Contents
- [Problem Statement](#problem_statement)
- [Idea / Solution](#idea)
- [Future Scope](#future_scope)
- [Deployment & Configuration](#deployment_config)
- [Usage](#usage)
- [Technology Stack](#tech_stack)
- [Authors](#authors)

## 🧐 Problem Statement <a name = "problem_statement"></a>
Ideally all of the available resources of a fog network should be utilized efficiently. Particularly  with a pay-per-use model, where resource utilization efficiency implies cost efficiency. This involves a mechanism to cope with fluidity of connected devices within the network.The network needs to adapt seamlessly, especially in a smart city environment, where mobile phones, cars or other moving smart objects are connected. Furthermore, applications that rely on low latency, like a traffic control system, need quick processing of the data at the edge. This is also required for sensitive data, that should not be transferred farther away from the data source than necessary. As many smart city application span across a large area, locality of nodes should also be incorporated in scheduling and placement decisions. Finally, for services like traffic control, availability is crucial. Thus, availability must always be given, even in the event of network failures. 

A centralised management of the fog network would yield the most efficient resource allocation, as scheduling mechanisms can optimize with universal knowledge about the network. But this central component represents a bottleneck, if all traffic needs to be directed towards the central component. Also, if services depend on a central component, availability may be reduced if network failures become more dominant, which is the case for large environments. Decentralized components within the network may not achieve overall efficiency, but can reduce network bandwidth usage, latency at the edge and availability, as they even run when disconnected from a central component. Especially in geo-distributed networks, decentralized components allow to incorporate locality of nodes into their scheduling decisions. However, relying on a static, decentralized management of the network does not take imbalanced load patterns and network changes into account. For example, a traffic control system may encounter bulk requests from a street with lots of traffic while somewhere else, little requests arrive. In such a scenario, a Kubernetes scheduler would have too many pending pods and thus latency will increase.

## 💡 Idea / Solution <a name = "idea"></a>
To achieve both, low latency at the edge and high availability, we use a hybrid solution with groups composed of Kubernetes clusters that communicate to exchange nodes. Kubernetes has already proven to reach efficient resource allocation and fault tolerance within a cluster. To mitigate the problem of pending pods, and thus increase availability, the clusters can exchange nodes to gain more resources. New nodes will be chosen decentralized among the clusters based on latency and the current load. 

## 🚀 Future Scope <a name = "future_scope"></a>
@berit add here

## 🏁 Deployment & Configuration <a name = "deployment_config"></a>
These instructions will get the project up and running.

### Prerequisites

- Install and configure Ansible

  ```shell
  apt-get install ansible
  ansible-galaxy collection install google.cloud
  ```

- Create a google cloud serviceaccount by following [this](https://alex.dzyoba.com/blog/gcp-ansible-service-account/) tutorial

- Open ports in the google cloud firewall to allow for external requests

  ```shell
  gcloud compute firewall-rules create cluster-flask --allow tcp:5000
  gcloud compute firewall-rules create kubectl-flask --allow tcp:5001
  ```

### Deployment

##### Cloud

- To deploy the cloud script in a compute instance, run `ansible-playbook ansible/deploy-cloud.yml -i ansible/inventory/gcp.yml`
- To configure the cloud, fill the placeholders in `/util/cloud_and_cluster_data.py` and run `/util/init_all.py`. Note that this also configures the clusters.
- To teardown the cloud, run `ansible-playbook ansible/destroy-cloud.yml -i ansible/inventory/gcp.yml`

##### Clusters

- Provisioning: `ansible-playbook ansible/create-k8s.yml -i ansible/inventory/gcp.yml`

- The following instructions should be repeated :repeat: for every cluster.

  ```shell
  gcloud container clusters get-credentials <cluster-name> --zone <zone> --project <google-cloud-project-name>
  
  arkade install openfaas --load-balancer
  kubectl rollout status -n openfaas deploy/gateway
  
  # in a second terminal ..
  kubectl port-forward svc/gateway -n openfaas 8080:8080
  
  # Logging into faas-cli
  # In the original terminal ..
  export OPENFAAS_URL="127.0.0.1:8080"
  PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
  echo -n $PASSWORD | faas-cli login --username admin --password-stdin
  
  # Checking if login was successful
  faas-cli list
  
  # Necessary to enable cluster surveillance
  kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
  
  # Inside /cluster directory ..
  docker build -t cluster-app .
  docker tag cluster-app pjdsgrouping/cluster-app
  docker push pjdsgrouping/cluster-app
  # In case the cluster-app was already deployed. Wait until gone!
  kubectl delete -n default deployment cluster-app
  kubectl create -f cluster-deployment.yml
  kubectl apply -f cluster-service.yml
  
  # In /kubectl-pod directory
  docker build -t kubectl-gcloud-pod .
  docker tag kubectl-gcloud-pod pjdsgrouping/kubectl-gcloud-pod
  docker push pjdsgrouping/kubectl-gcloud-pod
  # In case the kubectl-gcloud-pod was already deployed. Wait until gone!
  kubectl delete -n default deployment kubectl-gcloud-pod
  ./deploy-pod.sh <cluster-name> <zone>
  kubectl apply -f kubectl-service.yml
  # Execute the following only if kubectl needs to be accessible from the outside
  kubectl apply -f kubectl-service-public.yml
  ```

- To further configure all clusters, fill the placeholders in `/util/cloud_and_cluster_data.py` and run `/util/init_all.py`. Note that this also configures the cloud.

- Teardown: `ansible-playbook ansible/destroy-k8s.yml -i ansible/inventory/gcp.yml`

## 🎈 Usage <a name="usage"></a>
After successful deployment, the project code will autonomously take care of moving resources to the clusters with high load. Workflows of functions can now be batch deployed through the `/deploy-functions` cloud endpoint.

Sample request:

```http
POST http://<cloud_ip>:5000/deploy-functions"
```

```json
{
    "ip": "<target_cluster_ip>",
    "functions": [
        {
            "name": "first_function_name",
            "registry_url": "<docker_hub_registry_url>"
        },
        {
            "name": "second_function_name",
            "registry_url": "<docker_hub_registry_url>"
        }
    ]
}
```
_Example registry URL:_ `pjdsgrouping/ping-pong`

All functions will subsequently be deployed. A sample deployment script can be found at `/util/batch_deploy_functions.py`.

## ⛏️ Built With <a name = "tech_stack"></a>
- [Kubernetes](https://kubernetes.io/) - Container Orchestration
- [OpenFaaS](https://www.openfaas.com/) - FaaS Framework
- [Docker](https://www.docker.com/) - Containerization
- [Google Cloud](https://cloud.google.com/) - Infrastructure
- [Ansible](https://www.ansible.com/) - Infrastructure Provisioning and Configuration

## ✍️ Authors <a name = "authors"></a>
- [Berit Frech](https://github.com/bfrech)
- [Victor Bieszka](https://github.com/BieVic)
- [Christopher Woggon](https://github.com/chrissy0)
