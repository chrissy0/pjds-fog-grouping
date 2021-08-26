# Setup
- `ansible-playbook ansible/create-k8s.yml -i ansible/inventory/gcp.yml`
- `gcloud container clusters get-credentials pjds-cluster-1 --zone europe-west2-c --project pjds-fog-grouping` (for 2nd: `pjds-cluster-2`)
- `kubectl get nodes` (just to test the setup was successful)
- `arkade install openfaas --load-balancer`
- `kubectl rollout status -n openfaas deploy/gateway`
- `kubectl port-forward svc/gateway -n openfaas 8080:8080` (access ui @ localhost:8080, for 2nd: 8081:8080)

Get password:
```shell script
export OPENFAAS_URL="127.0.0.1:8080" # For 2nd, :8081

# This command retrieves your password
PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)

# This command logs in and saves a file to ~/.openfaas/config.yml, only execute echo-n $PASSWORD to print password
echo -n $PASSWORD | faas-cli login --username admin --password-stdin
```

- `faas-cli list` (test faas-cli after login)

# Teardown
- `ansible-playbook ansible/create-k8s.yml -i ansible/inventory/gcp.yml`

# Misc
Guide used: https://faun.pub/how-to-automate-the-setup-of-a-kubernetes-cluster-on-gcp-e97918bf41de