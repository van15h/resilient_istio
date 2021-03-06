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
# read urls of services from env variables
# service discovery based on kubernetes services
dest_analysis = os.environ.get('URL_IMAGE_ANALYZE',
                               'http://image-analysis:8080/frame')
dest_face = os.environ.get('URL_FACE_RECOGNITION',
                           'http://face-recognition:8080/frame')
dest_alerts = os.environ.get('URL_ALERTS',
                             'http://alerts:8080')
dest_momentum = os.environ.get('URL_MOMENTUM',
                             'http://momentm:8080/analysis')
# to switch between istio recommended FQDN and local development
k8s_suffix = os.environ.get('URL_K8S_SUFFIX', '')
# to allow faulty healthcheck
health_code = 200
pod_name = os.environ.get('MY_POD_NAME', 'collector')


@app.route('/fault', methods=['GET'])
def fault():
    """response health with fault 500"""
    global health_code
    if (health_code == 200):
        health_code = 503
        return Response('Now faulty', status=200)
    else:
        health_code = 200
        return Response('Now normal', status=200)


@app.route('/status', methods=['GET'])
def health():
    """health check"""
    if (health_code == 200):
        return Response('Collector ' + version + ' : Online - ' + pod_name,
                        mimetype='text/plain',
                        status=200)
    else:
        return Response('Collector ' + version + ' : Error 503 - ' + pod_name,
                        mimetype='text/plain',
                        status=503)


@app.route('/frame', methods=['POST'])
def forward_frame():
    """forward frame from camera to face recognition and image analysis"""
    if (request.is_json == True):
        app.logger.debug('post from agent is json')
        forward_analysis(request.json)
        forward_face(request.json)
    else:
        return Response('', status=400)
    return Response('', status=200)


def forward_analysis(frame):
    """forward to image analysis"""
    try:
        res = requests.post(dest_analysis, json=frame)
    except:
        app.logger.error('Failed to reach [' + dest_analysis + ']')
        return Response('', status=400)
    app.logger.debug('forwarded to: ' + dest_analysis)
    if (res.status_code == 200):
        forward_section(json.loads(res.text), frame['section'])
        forward_momentum_analysis(frame, json.loads(res.text))


def forward_momentum_analysis(frame, stats):
    """forward frame to cpanel with analyzed statistics"""
    if (len(stats['persons']) == 0):
        frame['persons'] = 'failed to analyze'
    elif (frame['timestamp'] == stats['persons'][0]['timestamp']):
        frame['persons'] = stats['persons']
    try:
        requests.post(dest_momentum, json=frame)
    except:
        app.logger.error('Failed to reach [' + dest_momentum + ']')
        return Response('', status=400)


def forward_section(obj, id):
    """forward response from image analyzer to proper section #id"""
    dest_section = 'http://section-' + str(id) + k8s_suffix + ':8080/persons'
    try:
        requests.post(dest_section, json=obj)
        app.logger.debug('forwarded to: ' + dest_section)
    except:
        app.logger.error('Failed to reach [' + dest_section + ']')
        return Response('', status=400)
    return Response('', status=200)


def forward_face(obj):
    """"forward frame to face recognition with destination - alerts"""
    try:
        obj['destination'] = dest_alerts
        del obj['persons']
        requests.post(dest_face, json=obj)
        app.logger.debug('forwarded to: ' + dest_face)
    except:
        print('Error: Failed to reach [' + dest_face + ']')
        return Response('', status=400)
    return Response('', status=200)


if __name__ == '__main__':
    app.run(host=bind_to['hostname'], port=int(bind_to['port']), debug=True)
