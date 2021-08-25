# Setup
- `ansible-playbook ansible/create-k8s.yml -i ansible/inventory/gcp.yml`
- ` gcloud container clusters get-credentials pjds-cluster-1 --zone europe-west2-c --project pjds-fog-grouping`
- `kubectl get nodes`

# Teardown
- `ansible-playbook ansible/create-k8s.yml -i ansible/inventory/gcp.yml`