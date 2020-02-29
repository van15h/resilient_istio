#!/usr/bin/env bash
#
# load generating script with fortio

FORTIO_POD=$(kubectl get pod | grep fortio | awk '{ print $1 }')
echo "fortio pod: " "${FORTIO_POD}"
echo "generating load to cpanel"
kubectl exec -it "${FORTIO_POD}"  -c fortio /usr/bin/fortio -- load -c 2 -qps 0 -n 20 -loglevel Warning http://cpanel:8080/