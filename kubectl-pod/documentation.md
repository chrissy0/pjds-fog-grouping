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
