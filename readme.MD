# PJDS Fog Grouping
## Cloud
#### Deployment
- `ansible-playbook ansible/deploy-cloud.yml -i ansible/inventory/gcp.yml`

Upon error (remote host identification has changed), reset known hosts
- `mv ~/.ssh/known_hosts ~/.ssh/known_hosts.bak`
#### Teardown
- `ansible-playbook ansible/destroy-cloud.yml -i ansible/inventory/gcp.yml`

## Cluster
#### Deployment
```shell
ansible-playbook ansible/create-k8s.yml -i ansible/inventory/gcp.yml

# Only 1x per google cloud account
gcloud compute firewall-rules create cluster-flask --allow tcp:5000
gcloud compute firewall-rules create kubectl-flask --allow tcp:5001

# (for 2nd: `pjds-cluster-2`)
mv ~/.kube/config ~/.kube/config.bak
gcloud container clusters get-credentials pjds-cluster-1 --zone europe-west2-c --project pjds-fog-grouping-326209
mv ~/.kube/config ~/.kube/config.bak
gcloud container clusters get-credentials pjds-cluster-2 --zone europe-west2-c --project pjds-fog-grouping-326209

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
cd cluster
docker build -t cluster-app .
docker tag cluster-app pjdsgrouping/cluster-app
docker push pjdsgrouping/cluster-app
kubectl delete -n default deployment cluster-app


# WAIT


#kubectl delete pod cluster-app-pod
kubectl create -f cluster-deployment.yml
kubectl apply -f cluster-service.yml
cd ..
# get public ip:
kubectl get svc

kubectl port-forward cluster-app-pod 5000

# kubectl-pod
cd kubectl-pod
cp ~/.kube/config config
# The next part is for some reason only necessary sometimes? If it doesn't work, replace `1001` by `$UID`
sudo chown 1001 config
# If there is an error, try get-credentials again
#cp -r /usr/lib/google-cloud-sdk/bin/ bin
#sudo chown 1001 bin/

docker build -t kubectl-pod .
docker tag kubectl-pod pjdsgrouping/kubectl-pod
docker push pjdsgrouping/kubectl-pod
kubectl delete -n default deployment kubectl-pod


# WAIT



#kubectl delete pod kubectl-pod
kubectl create -f kubectl-pod-deployment.yml

# setup service to access kubectl-pod:
kubectl apply -f kubectl-service.yml
# TODO Execute the following only if kubectl needs to be accessible from the outside
kubectl apply -f kubectl-service-public.yml
cd ..
# later: kubectl port-forward kubectl-pod 5001
# get static ip of kubectl-pod
kubectl get service kubectl-service --output yaml | grep clusterIP:
```
Get OpenFaas gateway IP: `kubectl get -n openfaas svc/gateway-external`

SSH into kubectl-pod: `kubectl exec --stdin --tty kubectl-pod -- /bin/ash`

If kubectl doesn't work, `mv ~/.kube/config ~/.kube/config.bak` and reload config using get-credentials

Get deployments: `kubectl get deployments --all-namespaces`

#### Draining a node
```shell
# TODO remove "--delete-local-data" from command?
kubectl drain gke-pjds-cluster-1-node-pool-pjds-clu-35b0997a-jg19 --ignore-daemonsets --delete-local-data --force
```

#### Teardown
```shell
ansible-playbook ansible/destroy-k8s.yml -i ansible/inventory/gcp.yml
```