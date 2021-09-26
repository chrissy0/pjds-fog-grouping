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
