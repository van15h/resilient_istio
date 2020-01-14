#!/bin/sh
ISTIO_VERSION=1.4.3
curl -O https://github.com/istio/istio/releases/download/$ISTIO_VERSION/istio-$ISTIO_VERSION-linux.tar.gz
curl -O https://github.com/istio/istio/releases/download/$ISTIO_VERSION/istio-$ISTIO_VERSION-linux.tar.gz.sha256
ls -la istio-*
echo "check data integrity"
#export vars
#kubectl label namespace default istio-injection=enabled
#kubectl get namespace -L istio-injection
