#!/usr/bin/env bash
#
# setup ennv variables for current shell

# get and export minikube ip and port
echo "export ip and port of istio ingress to env variables"
source exports.sh
echo "INGRESS_HOST=$INGRESS_HOST, INGRESS_PORT=$INGRESS_PORT"

# generate env variable of minikube ip and port
echo "creating url.js file with ip and port"
{
echo "url = {" ;
echo "  HOST: '$INGRESS_HOST'," ;
echo "  PORT: '$INGRESS_PORT'" ;
echo "}"
} >> src/cpanel_v1/static/scripts/url_env.js

cp src/cpanel_v1/static/scripts/url_env.js src/cpanel_v2/static/scripts/url_env.js
