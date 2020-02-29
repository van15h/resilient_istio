#!/usr/bin/env bash
#
# deploy fortio load generator

kubectl apply -f <(istio-1.4.3/bin/istioctl kube-inject -f istio-1.4.3/samples/httpbin/sample-client/fortio-deploy.yaml)
FORTIO_POD=$(kubectl get pod | grep fortio | awk '{ print $1 }')
echo "fortio pod: " "${FORTIO_POD}"
echo "get response from cpanel"
kubectl exec -it "${FORTIO_POD}"  -c fortio /usr/bin/fortio -- load -curl  http://cpanel:8080/status