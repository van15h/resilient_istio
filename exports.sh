#!/usr/bin/env bash
INGRESS_HOST=$(minikube ip -p testvm)
INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')