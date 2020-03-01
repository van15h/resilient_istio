from flask import Flask, request, Response
import requests
import json
import pathlib
import logging
import os

app = Flask(__name__)

# server listen port
port = int(os.environ.get('PORT', 8080))
bind_to = {'hostname': '0.0.0.0', 'port': port}
# app version
version = os.environ.get('VERSION', 'v1')

stats_analysis = {
    'persons': [
        {
            'age': 'empty',
            'gender': 'empty',
            'event': 'empty',
            'timestamp': 'empty'
        },
    ]}
stats_alert = stats_analysis


@app.route('/status', methods=['GET'])
def health():
    """health check"""
    return Response('Momentum ' + version + ' : Online',
                    status=200,
                    mimetype='text/plain')


@app.route('/analysis', methods=['POST'])
def post_analysis():
    """to recieve statistic about frame from image analysis"""
    global stats_analysis
    if (request.is_json == True):
        app.logger.debug('got statistic from analysis')
        app.logger.debug('analysis timestamp:'
                         + str(request.json['timestamp']))
        stats_analysis = request.json
    else:
        return Response('', status=400)
    return Response('', status=200)


@app.route('/alert', methods=['POST'])
def post_alert():
    """to recieve the latest alert"""
    global stats_alert
    if (request.is_json == True):
        app.logger.debug('got alert from face recognition')
        app.logger.debug('alert timestamp: '
                         + request.json['timestamp'])
        stats_alert = request.json
    else:
        return Response('', status=400)
    return Response('', status=200)


@app.route('/analysis', methods=['GET'])
def get_analysis():
    """returns info from image analysis for most recent frame"""
    app.logger.debug('get analysis for current frame')
    app.logger.debug('analysis timestamp:'
                     + stats_analysis['timestamp'])
    headers = [{'Access-Control-Allow-Origin', '*'}]
    return Response(json.dumps(stats_analysis, indent=2),
                    status=200,
                    headers=headers)


@app.route('/alert', methods=['GET'])
def get_current_alert():
    """returns info from most recent alert"""
    app.logger.debug('get alert for current frame')
    app.logger.debug('alert timestamp: '
                     + stats_alert['timestamp'])
    headers = [{'Access-Control-Allow-Origin', '*'}]
    return Response(json.dumps(stats_alert, indent=2),
                    status=200,
                    headers=headers)


if __name__ == '__main__':
    app.run(host=bind_to['hostname'], port=int(bind_to['port']), debug=True)
