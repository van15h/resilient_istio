#!/usr/bin/env bash
#
# It is supposed, that minikube and curl are installed in your system
# Create minikube VM and download kubectl of the same version

# to make script exit when a command fails
set -o errexit
# to exit when script tries to use undeclared variables
set -o nounset

# current dir
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

main() {
  check_requirements

  local memory=16384
  local cpu=4
  local k8s_version="v1.15.7"
  local vm_name="airport"

  if create_minikube_vm && install_kubectl; then
    echo "proceed to next step from project README"
    echo "SUCCESS: minikube VM and kubectl configured"
  fi
}

create_minikube_vm() {
  # the name of VM is 'airport'
  # to avoid conflicts with possible local minikube installations
  echo "creating minikube VM"
  minikube start \
    -p "${vm_name}" \
    --vm-driver=virtualbox \
    --memory="${memory}" \
    --cpus="${cpu}" \
    --kubernetes-version="${k8s_version}"
}

install_kubectl() {
  # install kubectl
  echo "download kubectl of the same version as K8S"
  curl -LO https://storage.googleapis.com/kubernetes-release/release/"${k8s_version}"/bin/linux/amd64/kubectl
  echo "kubectl downloaded to ${__dir}"

  # check size of downloaded file
  local file="./kubectl"
  local min_size=30000000
  local size
  size=$(wc -c <"${file}")
  if [ "${size}" -ge "${min_size}" ]; then
    echo "make kubectl executable"
    chmod +x ./kubectl
    check_minikube_running
  else
    echo "Error: Kubectl file is not proper size"
    echo "Please download kubectl version ${k8s_version} manually:"
    echo "curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.15.7/bin/linux/amd64/kubectl"
    echo "to project location: ${__dir}"
    echo "Make it executable with:"
    echo "chmod +x ./kubectl"
    echo "FAILED: Kubectl file is not proper size"
    exit 1
  fi
}

check_requirements() {
  echo "check requirements"
}

check_minikube_running() {
  echo "minikube status:"
  minikube status -p "${vm_name}"
  echo "kubectl version:"
  ./kubectl version --client
  echo "kubernetes is up and running:"
  ./kubectl get namespaces
}

main
