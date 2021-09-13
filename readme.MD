# PJDS Fog Grouping
## Cloud
#### Deployment
- `ansible-playbook ansible/deploy-cloud.yml -i ansible/inventory/gcp.yml`

Upon error (remote host identification has changed), reset known hosts
- `mv ~/.ssh/known_hosts ~/.ssh/known_hosts.bak`

Get OpenFaas gateway IP: `kubectl get -n openfaas svc/gateway-external`
#### Teardown
- `ansible-playbook ansible/destroy-cloud.yml -i ansible/inventory/gcp.yml`

## Cluster
#### Deployment
```shell
ansible-playbook ansible/create-k8s.yml -i ansible/inventory/gcp.yml

gcloud compute firewall-rules create cluster-flask --allow tcp:5000
gcloud compute firewall-rules create kubectl-flask --allow tcp:5001

# (for 2nd: `pjds-cluster-2`)
gcloud container clusters get-credentials pjds-cluster-1 --zone europe-west2-c --project pjds-fog-grouping

# (just to test the setup was successful)
kubectl get nodes

arkade install openfaas --load-balancer
kubectl rollout status -n openfaas deploy/gateway

# (access ui @ localhost:8080, for 2nd: 8081:8080)
kubectl port-forward svc/gateway -n openfaas 8080:8080

# Get password (for 2nd, :8081)
export OPENFAAS_URL="127.0.0.1:8080"

# This command retrieves your password
PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)

# This command logs in and saves a file to ~/.openfaas/config.yml, only execute echo-n $PASSWORD to print password
echo -n $PASSWORD | faas-cli login --username admin --password-stdin

# (test faas-cli after login)
faas-cli list

kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Inside /cluster directory
docker build -t cluster-app .
docker tag cluster-app pjdsgrouping/cluster-app
docker push pjdsgrouping/cluster-app
kubectl delete pod cluster-app-pod
kubectl create -f deploy-cluster.yml
kubectl apply -f cluster-service.yml
# get public ip:
kubectl get svc

kubectl port-forward cluster-app-pod 5000

# kubectl-pod
cp ~/.kube/config config
# The next part is for some reason only necessary sometimes? If it doesn't work, replace `1001` by `$UID`
sudo chown 1001 config
# If there is an error, try get-credentials again
docker build -t kubectl-pod .
docker tag kubectl-pod pjdsgrouping/kubectl-pod
docker push pjdsgrouping/kubectl-pod
kubectl delete pod kubectl-pod
kubectl create -f deploy-kubectl-pod.yml
# later: kubectl port-forward kubectl-pod 5001

# setup service to access kubectl-pod:
kubectl apply -f kubectl-service.yml
# get static ip of kubectl-pod
kubectl get service kubectl-service --output yaml | grep clusterIP:
```

#### Teardown
```shell
ansible-playbook ansible/destroy-k8s.yml -i ansible/inventory/gcp.yml
```