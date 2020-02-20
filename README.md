# Resilient istio (in progress...)

Resilient deployment of microservices applications with Kubernetes and Istio

## Requirements

+ linux

+ virtualbox

+ minikube

+ curl

## How to run

+ clone the project. run: `git clone git@github.com:van15h/resilient_istio.git`

+ go to project folder: `cd resilient_istio`

+ create minikube VM. run: `./create_minikube_cluster.sh`

+ install and deploy istio to minikube. run `./install_istio.sh`

+ to use k8s docker locally. images will be built direct in minikube VM.
    run: `eval $(minikube docker-env -p airport)`

+ to get minikube ip and port as environment variable run: `./generate_minikube_url.sh`

+ build docker containers locally. run: `./build_containers.sh`

+ use `Makefile` to deploy app

+ use `Makefile` to play around Istio resilliency

+ cleanup all. run: `./cleanup.sh`
