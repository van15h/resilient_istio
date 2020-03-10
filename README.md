# Resilient deployments with Istio service mesh

## Requirements

Virtual machine to run Minikube cluster need at least 4 CPU and 8GB RAM ( default configuration in installation scripts is 4 CPU and 16GB RAM).

+ linux

+ virtualbox

+ minikube

+ curl

## How to run

+ clone the project with (if SSH is configured, otherwise change to HTTPS link):

```sh
git clone git@github.com:van15h/resilient_istio.git
```

+ go to project folder:

```sh
cd resilient_istio
```

+ create Minikube virtual machine with:

```sh
./create_minikube_cluster.sh
```

+ install and deploy istio to Minikube with:

```sh
./install_istio.sh
```

+ to use Docker engine from Minikube locally run:

```sh
eval $(minikube docker-env -p airport)
```

+ export variables for local bash with:

```sh
export INGRESS_HOST=$(minikube ip -p airport)
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
echo "INGRESS_HOST=$INGRESS_HOST, INGRESS_PORT=$INGRESS_PORT"
```

+ after all istio services are up and running to get Minikube IP and port as environment variable run for current shell session run:

```sh
./generate_minikube_url.sh
```

+ to build Docker images and make them available in Minikube run:

```sh
./build_containers.sh
```

The images are also available in Docker hub, but there is a need to build control panel locally, because Minikube IP address is used in dashboard and should be injected in the code. It is work around to not to change the Linux hosts configuration file.

+ use Makefile to deploy the application

+ use Makefile to try out Istio resilliency features

+ to cleanup all run:

```sh
./cleanup.sh
```
