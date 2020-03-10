#!/usr/bin/env bash
#
# cleanup the develeopment environment

echo "stopping minikube cluster.."
minikube stop -p airport
echo "deleting minikube cluster.."
minikube delete -p airport

echo "please delete the project folder by yourself"
echo "following commands can be helpful"
echo "run: cd .."
echo "run: rm -r resilient_istio"
echo "or just use your file manager"