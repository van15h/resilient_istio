#!/usr/bin/env bash
#
# cleanup temp data

# delete alerts data
echo "deleting alerts..."
rm -rf src/alerts/data_alerts.json
# delete detected statistical analysis data
echo "deleting statistics..."
rm -rf src/section/data_persons_1.json