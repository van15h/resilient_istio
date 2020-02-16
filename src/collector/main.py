from flask import Flask, request, abort, Response
import requests
import json
import pathlib
import logging
import os

app = Flask(__name__)

port = int(os.environ.get('PORT', 8080))
bind_to = {'hostname': '0.0.0.0', 'port': port}

# read urls of services from env variables
dest_analysis = os.environ.get('URL_IMAGE_ANALYZE',
                               'http://image-analysis:8080/frame')
dest_face = os.environ.get('URL_FACE_RECOGNITION',
                           'http://face-recognition:8080/frame')
dest_alerts = os.environ.get('URL_ALERTS',
                             'http://alerts:8080')
dest_cpanel = os.environ.get('URL_CPANEL',
                             'http://cpanel:8080/analysis')


@app.route('/status', methods=['GET'])
def show_status():
    return Response('Collector : Online', status=200, mimetype='text/plain')


@app.route('/frame', methods=['POST'])
def forward_frame():
    """forward frame from camera to face recognition and image analyzer"""
    if (request.is_json == True):
        app.logger.debug('post from agent is json')
        forward_analysis(request.json)
        forward_face(request.json)
    else:
        return Response('', status=400)
    return Response('', status=200)


def forward_analysis(frame):
    """forward to image analyzer"""
    try:
        res = requests.post(dest_analysis, json=frame)
    except:
        app.logger.error('Failed to reach [' + dest_analysis + ']')
        return Response('', status=400)
    app.logger.debug('forwarded to: ' + dest_analysis)
    if (res.status_code == 200 ):
        forward_section(json.loads(res.text), frame['section'])
        forward_cpanel_analysis(frame, json.loads(res.text))


def forward_cpanel_analysis(frame, stats):
    """forward frame to cpanel with analyzed statistics"""
    if (len(stats['persons']) == 0):
        frame['persons'] = 'failed to analyze'
    elif (frame['timestamp'] == stats['persons'][0]['timestamp']):
        frame['persons'] = stats['persons']
    try:
        requests.post(dest_cpanel, json=frame)
    except:
        app.logger.error('Failed to reach [' + dest_cpanel + ']')
        return Response('', status=400)


def forward_section(obj, id):
    """forward response from image analyzer to proper section #id"""
    dest_section = 'http://section-' + str(id) + ':8080/persons'
    try:
        requests.post(dest_section, json=obj)
        app.logger.debug('forwarded to: ' + dest_section)
    except:
        app.logger.error('Failed to reach [' + dest_section + ']')
        return Response('', status=400)
    return Response('', status=200)


def forward_face(obj):
    """"forward frame to face recognition with response destination - alerts"""
    try:
        obj['destination'] = dest_alerts
        requests.post(dest_face, json=obj)
        app.logger.debug('forwarded to: ' + dest_face)
    except:
        print('Error: Failed to reach [' + dest_face + ']')
        return Response('', status=400)
    return Response('', status=200)


if __name__ == '__main__':
    app.run(host=bind_to['hostname'], port=int(bind_to['port']), debug=True)
