# Setup
- `ansible-playbook ansible/create-k8s.yml -i ansible/inventory/gcp.yml`
- ` gcloud container clusters get-credentials pjds-cluster-1 --zone europe-west2-c --project pjds-fog-grouping`
- `kubectl get nodes`

# Teardown
- `ansible-playbook ansible/create-k8s.yml -i ansible/inventory/gcp.yml`

# Misc
Guide used: https://faun.pub/how-to-automate-the-setup-of-a-kubernetes-cluster-on-gcp-e97918bf41de