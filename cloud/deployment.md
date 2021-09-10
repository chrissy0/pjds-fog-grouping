# Compute Instance (Ansible)
## Deployment
- `ansible-playbook ansible/deploy-cloud.yml -i ansible/inventory/gcp.yml`
## Teardown
- `ansible-playbook ansible/destroy-cloud.yml -i ansible/inventory/gcp.yml`
# Kubernetes (not used)
- `docker build -t cloud-app .`
- `docker tag cloud-app pjdsgrouping/cloud-app`
- `docker push pjdsgrouping/cloud-app`
- `kubectl create -f deploy-cloud.yml`
- `kubectl port-forward cloud-app-pod 5000`
Now the cloud is accessible at localhost:5000


Get OpenFaas gateway IP: `kubectl get -n openfaas svc/gateway-external`