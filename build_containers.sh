#!/usr/bin/env bash
#
# build containers locally

echo "building alerts v1"
docker build -t van15h/alerts:v1 src/alerts

echo "building cpanel v1"
docker build -t van15h/cpanel:v1 src/cpanel_v1

echo "building cpanel v2"
docker build -t van15h/cpanel:v2 src/cpanel_v2

echo "building section v1"
docker build -t van15h/section:v1 src/section

echo "building collector v1"
docker build -t van15h/collector:v1 src/collector

echo "building momentum v1"
docker build -t van15h/momentum:v1 src/momentum

echo "check if all containers built"
docker images | grep 'alerts\|cpanel\|collector\|section\|momentum'
