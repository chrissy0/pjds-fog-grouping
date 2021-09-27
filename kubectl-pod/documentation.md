- `cp ~/.kube/config config`
The next part is for some reason only necessary sometimes? If it doesn't work, replace `1001` by `$UID`
- `sudo chown 1001 config`
If there is an error, rerun get-credentials

- `docker build -t kubectl-gcloud-pod .`
- `docker tag kubectl-pod pjdsgrouping/kubectl-gcloud-pod`
- `docker push pjdsgrouping/kubectl-gcloud-pod`
- `./deploy-pod.sh <cluster-name> <zone>`
- `kubectl port-forward kubectl-gcloud-pod 5001`

## Endpoints

#### POST: ```/delete-node```

```json
{
  "node": "<node-name>"
}
```

#### GET: ```/add-node```
