#!/usr/bin/env bash
#
# cleanup temp data

# delete alerts data
echo "deleting alerts... : ./src/alerts/data_alerts.json"
rm -rf src/alerts/data_alerts.json
# delete detected statistical analysis data
echo "deleting statistics... : ./src/section/data_persons_1.json"
rm -rf src/section/data_persons_1.json