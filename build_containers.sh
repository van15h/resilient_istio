#!/usr/bin/env bash
#
# build containers locally

echo "building alerts v1"
docker build -t van15h/alerts:v1 src/alerts

echo "building cpanel v1"
docker build -t van15h/cpanel:v1 src/cpanel

echo "building section v1"
docker build -t van15h/section:v1 src/section

echo "building collector v1"
docker build -t van15h/collector:v1 src/collector

echo "check if all 4 containers built"
docker images | grep 'alerts\|cpanel\|collector\|section'
