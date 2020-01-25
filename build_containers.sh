#!/usr/bin/env bash
#
#

echo "building alerts v1"
docker build -t alerts:v1 src/alerts

echo "building cpanel v1"
docker build -t cpanel:v1 src/cpanel

echo "building section v1"
docker build -t section:v1 src/section

echo "building collector v1"
docker build -t collector:v1 src/collector

echo "check if all 4 containers built"
docker images | grep 'alerts\|cpanel\|collector\|section'
