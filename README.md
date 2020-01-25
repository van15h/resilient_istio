# Resilient istio (in progress...)

Resilient deployment of microservices applications with Kubernetes and Istio

## Requirements

+ curl

+ virtualbox

+ minikube

## How to run

+ clone the project. run: `git clone git@github.com:van15h/resilient_istio.git`

+ go to project folder: `cd resilient_istio`

+ create minikube VM. run: `./create_minikube_cluster.sh`

+ to use k8s docker locally. images will be built direct in minikube VM.
    run: `eval $(minikube docker-env -p airport)`

+ build docker containers locally. run: `./build_containers.sh`

+ use `Makefile` to deploy app

+ use `Makefile` to play around Istio resilliency

+ cleanup all. run: `./cleanup.sh`
