#!/bin/sh

sed -e 's|<CLUSTER>|"'$1'"|g; s|<ZONE>|"'$2'"|g' kubectl-pod-deployment.yml | kubectl apply -f -
kubectl apply -f kubectl-service.yml