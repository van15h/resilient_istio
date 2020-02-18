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
