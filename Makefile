run-mini:
	minikube start -p testvm --kubernetes-version=v1.15.7

stop-mini:
	minikube stop -p testvm

ssh:
	minikube ssh -p testvm

load:
	for i in {1..100}; do sleep 0.2; curl http://$(INGRESS_HOST):$(INGRESS_PORT)/status; printf "\n"; done

start-cameras:
	curl http://$(INGRESS_HOST):$(INGRESS_PORT)/production?toggle=on

stop-cameras:
	curl http://$(INGRESS_HOST):$(INGRESS_PORT)/production?toggle=off

health:
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

deploy-app-default:
	./kubectl apply -f k8s
	./kubectl get pods --watch

deploy-istio-default:
	./kubectl apply -f istio/dest_rule_all.yaml
	./kubectl apply -f istio/virt_svc_all.yaml
	./kubectl apply -f istio/ingress_gateway.yaml

cpanel-50-50:
	./kubectl apply -f istio/virt_svc_50-50.yaml

cpanel-v2:
	./kubectl apply -f istio/virt_svc_v2.yaml

scale_v2_x3:
	./kubectl scale deployment cpanel-v2 --replicas=3

scale_v2_x1:
	./kubectl scale deployment cpanel-v2 --replicas=1

scale_deployment:
	./kubectl scale deployment collector --replicas=2
	./kubectl scale deployment image-analysis --replicas=2
	./kubectl scale deployment face-recognition --replicas=2

round_robin:
	./kubectl apply -f istio/round_robin.yaml

random:
	./kubectl apply -f istio/random_lb.yaml

fault-injection-500:
	./kubectl apply -f istio/fault_injection-500.yaml

fault-injection-delay10:
	./kubectl apply -f istio/fault_injection-delay10.yaml

get-istio:
	./kubectl get pods -n istio-system

timeout:
	./kubectl apply -f istio/timeout.yaml

retries:
	./kubectl apply -f istio/retry.yaml

health-retries:
	for i in {1..10}; do sleep 0.2; curl http://$(INGRESS_HOST):$(INGRESS_PORT)/sections/1/status; printf "\n"; done

health-timeout:
	for i in {1..10}; do sleep 0.2; curl http://$(INGRESS_HOST):$(INGRESS_PORT)/cameras/1/state; printf "\n"; done

get-all:
	./kubectl get pods
	./kubectl get services
	./kubectl get destinationrules
	./kubectl get virtualservices
	./kubectl get gateways