#!/usr/bin/env bash
#
# deploy fortio load generator

kubectl apply -f <(istio-1.4.3/bin/istioctl kube-inject -f istio-1.4.3/samples/httpbin/sample-client/fortio-deploy.yaml)
FORTIO_POD=$(./kubectl get pod -l app=fortio -o jsonpath='{.items[0].metadata.name}')
echo "fortio pod: " "${FORTIO_POD}"
echo "get response from collector"
kubectl exec -it "${FORTIO_POD}"  -c fortio /usr/bin/fortio -- load -curl  http://collector:8080/status
echo