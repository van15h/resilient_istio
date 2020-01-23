#!/bin/sh

MEMORY=16384
CPU=4
K8S_VERSION="v1.15.7"

# the name of VM is 'airport'
# to avoid conflicts with possible local minikube installations
echo "create minikube VM"
#minikube start -p airport --vm-driver=virtualbox --memory=$MEMORY --cpus=$CPU --kubernetes-version=$K8S_VERSION

# install kubectl
echo "download kubectl of the same version as K8S"
curl -LO https://storage.googleapis.com/kubernetes-release/release/$K8S_VERSION/bin/linux/amd64/kubectl
echo "make kubectl executable"
# check if downloaded successful
FILE="./kubectl"
MIN_SIZE=9000000
SIZE=$(wc -c <"$FILE")
if [ "$SIZE" -ge "$MIN_SIZE" ]; then
  chmod +x ./kubectl
else
  echo "Error: Kubectl file not found"
  echo "Please download kubectl version $K8S_VERSION manually:"
  echo "curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.15.7/bin/linux/amd64/kubectl"
  echo "Make it executable with:"
  echo "chmod +x ./kubectl"
fi
# sudo mv ./kubectl /usr/bin/kubectl
