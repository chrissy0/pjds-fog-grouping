- `cp ~/.kube/config config`
The next part is for some reason only necessary sometimes? If it doesn't work, replace `1001` by `$UID`
- `sudo chown 1001 config`
If there is an error, rerun get-credentials

- `docker build -t kubectl-pod .`
- `docker tag kubectl-pod pjdsgrouping/kubectl-pod`
- `docker push pjdsgrouping/kubectl-pod`
- `kubectl create -f deploy-kubectl-pod.yml`
- `kubectl port-forward kubectl-pod 5001`

## Endpoints

Before using the kubectl pod, set the configs by using the ```/set-config``` endpoint. The cluster name needs to be set manually, since the pods are running in different clusters. The zone name could possibly be extracted when the cluster name is known. Let me(Victor) know if I should implement this.

#### POST: ```/set-config```

```json
{
  "cluster": "<cluster-name>",
  "zone": "<zone-name>"
}
```

#### POST: ```/delete-node```

```json
{
  "node": "<node-name>"
}
```

#### GET: ```/add-node```
