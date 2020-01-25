from flask import Flask, request, abort, Response
import requests
import json
import pathlib
import logging
import os

app = Flask(__name__)

bind_to = {'hostname': "0.0.0.0", 'port': 8080}

# read urls of services from env variables
dest_analysis = os.environ['URL_IMAGE_ANALYZE']
dest_face = os.environ['URL_FACE_RECOGNITION']
dest_alerts = os.environ['URL_ALERTS']


@app.route('/status', methods=['GET'])
def show_status():
    return Response("Collector : Online", status=200, mimetype="text/plain")


@app.route('/frame', methods=['POST'])
def forward_frame():
    """forward frame from camera to face recognition and image analyzer"""
    if (request.is_json == True):
        app.logger.debug('post from agent is json')
        id = request.json['section']
        forward_analysis(request.json, id)
        forward_face(request.json)
    else:
        return Response("", status=400)
    return Response("", status=200)


def forward_analysis(obj, id):
    """forward to image analyzer"""
    try:
        res = requests.post(dest_analysis, json=obj)
        app.logger.debug('forwarded to: ' + dest_analysis)
        forward_section(res, id)
    except:
        app.logger.error('Failed to reach [' + dest_analysis + ']')
        return Response("", status=400)


def forward_section(obj, id):
    """forward response from image analyzer to proper section #id"""
    dest_section = 'http://section-' + str(id) + ':8080/persons'
    try:
        requests.post(dest_section, json=json.loads(obj.text))
        app.logger.debug('forwarded to: ' + dest_section)
    except:
        app.logger.error('Failed to reach [' + dest_section + ']')
        return Response("", status=400)
    return Response("", status=200)


def forward_face(obj):
    """"forward frame to face recognition with response destination - alerts"""
    try:
        obj['destination'] = dest_alerts
        requests.post(dest_face, json=obj)
        app.logger.debug('forwarded to: ' + dest_face)
    except:
        print('Error: Failed to reach [' + dest_face + ']')
        return Response("", status=400)
    return Response("", status=200)


if __name__ == '__main__':
    app.run(host=bind_to['hostname'], port=int(bind_to['port']), debug=True)
