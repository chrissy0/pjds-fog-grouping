# Kubernetes
- `kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml`
- `docker build -t cluster-app .`
- `docker tag cluster-app pjdsgrouping/cluster-app`
- `docker push pjdsgrouping/cluster-app`
- `kubectl create -f deploy-cluster.yml`
- `kubectl port-forward cluster-app-pod 5000`
Now the cluster flask server is accessible at localhost:5000
# kubectl-pod
- `sudo chown 1001 ~/.kube/config`
- `docker run --rm --name kubectl -v ~/.kube/config:/.kube/config bitnami/kubectl:latest top nodes`
If there is an error, try get-credentials again