#!/usr/bin/env bash
#
# load generating script with fortio

FORTIO_POD=$(./kubectl get pod -l app=fortio -o jsonpath='{.items[0].metadata.name}')
echo "fortio pod: " "${FORTIO_POD}"
echo "generating load to cpanel"
kubectl exec -it "${FORTIO_POD}"  -c fortio /usr/bin/fortio -- load -c 3 -qps 0 -n 20 -loglevel Warning http://collector:8080/status