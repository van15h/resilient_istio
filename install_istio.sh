#!/usr/bin/env bash

# to make script exit when a command fails
set -o errexit
# to exit when script tries to use undeclared variables
set -o nounset

main(){
  local version="1.4.3"
  local name
  name="istio-${version}"
  local url="https://github.com/istio/istio/releases/download/${version}/istio-${version}-linux.tar.gz"

  download_istio

  deploy_istio

  echo "wait till all services go online: STATUS - Running"
  echo "./kubectl get pods -n istio-system"
  echo "proceed to next step from project README"
  echo "SUCCESS: istio installed"
}

download_istio(){
  echo "Downloading ${name} from ${url}"
  curl -L "${url}" | tar xz
  echo "export path variable to use istioctl"
  export PATH=$PWD/"${name}"/bin:$PATH
  istioctl verify-install
}

deploy_istio(){
  echo "enable auto sidecar injection"
  ./kubectl label namespace default istio-injection=enabled
  echo "check injection enabled"
  ./kubectl get namespace -L istio-injection
  echo "deploy istio services"
  istioctl manifest apply --set profile=demo
  echo "show deployed istio services"
  ./kubectl get services -n istio-system
}

main