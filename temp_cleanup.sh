#!/usr/bin/env bash
#
# cleanup temp data

echo "deleting alerts... : ./src/alerts/data_alerts.json"
rm -rf src/alerts/data_alerts.json

echo "deleting statistics... : ./src/section/data_persons_1.json"
rm -rf src/section/data_persons_1.json

echo "deleting js env variable for cpanel v1"
rm -rf src/cpanel_v1/static/scripts/url_env.js

echo "deleting js env variable for cpanel v2"
rm -rf src/cpanel_v2/static/scripts/url_env.js