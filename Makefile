IMAGE_NAME ?= sidecar-python
SHELL=bash

all: build kubeconf up trigger sleep watch-sidecar

.PHONY: install-astro
install-astro:
	brew install astronomer/cloud/astrocloud

.PHONY: up
up:
	astrocloud dev start

.PHONY: trigger
trigger:
	astrocloud dev run dags trigger sidecar_dag

.PHONY: sleep
sleep:
	echo waiting for a while for the sidecar to be available
	sleep 60

.PHONY: down
down: delp
	astrocloud dev stop

.PHONY: build
build:
	docker build -f python.Dockerfile -t "${IMAGE_NAME}" .

.PHONY: kubeconf
kubeconf:
	mkdir -p ./include/.kube
	cp ${HOME}/.kube/config ./include/.kube/config

.PHONY: watch-sidecar
watch-sidecar:
	${MAKE} watch CONT=sidecar

.PHONY: watch-base
watch-base:
	${MAKE} watch CONT=base

.PHONY: watch
CONT ?= base
watch:
	kubectl logs -f $(shell kubectl get pods | grep sidecar | awk '{print $$1}') "${CONT}"

.PHONY: delp
delp:
	kubectl delete pods $(shell kubectl get pods | grep sidecar | awk '{print $$1}')