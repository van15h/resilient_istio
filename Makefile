minikube:
	minikube start -p testvm --kubernetes-version=v1.15.7
lb:
	for i in {1..10}; do sleep 0.2; curl http://$(INGRESS_HOST):$(INGRESS_PORT)/status; printf "\n"; done

start-cameras:
	curl http://$(INGRESS_HOST):$(INGRESS_PORT)/production?toggle=on

stop-cameras:
	curl http://$(INGRESS_HOST):$(INGRESS_PORT)/production?toggle=off

status:
	curl http://$(INGRESS_HOST):$(INGRESS_PORT)/status
	@printf "\n"
	curl http://$(INGRESS_HOST):$(INGRESS_PORT)/cameras/1/state
	@printf "\n"
	curl http://$(INGRESS_HOST):$(INGRESS_PORT)/cameras/2/state
	@printf "\n"
	curl http://$(INGRESS_HOST):$(INGRESS_PORT)/collector/status
	@printf "\n"
	curl http://$(INGRESS_HOST):$(INGRESS_PORT)/alerts/status
	@printf "\n"
	curl http://$(INGRESS_HOST):$(INGRESS_PORT)/sections/1/status
	@printf "\n"

default-reset:
	./kubectl delete gateway --all
	./kubectl delete destinationrule --all
	./kubectl delete virtualservice --all

all-reset:
	./kubectl delete service --all
	./kubectl delete deployment --all
	./kubectl delete gateway --all
	./kubectl delete destinationrule --all
	./kubectl delete virtualservice --all

deploy-app:
	./kubectl apply -f k8s

destination-rules:
	./kubectl apply -f istio/dest_rule_all.yaml

virtual-services:
	./kubectl apply -f istio/virt_svc_all.yaml

ingress:
	./kubectl apply -f istio/ingress_gateway.yaml

cpanel-v2:
	./kubectl apply -f istio/virt_svc_v2.yaml

get-all:
	./kubectl get pods
	./kubectl get services
	./kubectl get destinationrules
	./kubectl get virtualservices
	./kubectl get gateways