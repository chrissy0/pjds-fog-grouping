https://github.com/stefanprodan/openfaas-gke
https://docs.openfaas.com/deployment/kubernetes/
https://docs.openfaas.com/reference/namespaces/

install and init gcloud (sdk)

install jq

Your Pod address range (`--cluster-ipv4-cidr`) can accommodate at most 1008 node(s).

gcloud container clusters create demo     --cluster-version=${k8s_version}     --zone=europe-west3-a     --num-nodes=2     --machine-type=n1-standard-2     --scopes=default,storage-rw

gcloud container clusters resize demo --num-nodes=8 --region=europe-west3-a

gcloud container clusters get-credentials demo -z=europe-west3-a

kubectl create clusterrolebinding "cluster-admin-$(whoami)" \
    --clusterrole=cluster-admin \
    --user="$(gcloud config get-value core/account)"

kubectl create clusterrolebinding kube-system-cluster-admin \
    --clusterrole cluster-admin \
    --user system:serviceaccount:kube-system:default

kubectl proxy --port=9099 &

arkade install openfaas --load-balancer

kubectl -n openfaas get deployments -l "release=openfaas, app=openfaas"

temporarily pause:
gcloud container clusters resize demo --num-nodes=0 --region=europe-west3-a

kubectl get -n openfaas svc/gateway-external

PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)

echo -n $PASSWORD