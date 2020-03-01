from flask import Flask, request, Response, render_template
import requests
import json
import pathlib
import logging
import os
import time

app = Flask(__name__)

# server port
port = int(os.environ.get('PORT', 8080))
bind_to = {'hostname': '0.0.0.0', 'port': port}
# app version
version = os.environ.get('VERSION', 'v1')
dest_alerts = os.environ.get('URL_ALERTS', 'http://alerts:8080')
dest_collector = os.environ.get('URL_COLLECTOR', 'http://collector:8080')
dest_momentum = os.environ.get('URL_MOMENTUM', 'http://momentum:8080')
# to switch between istio recommended FQDN and local development
k8s_suffix = os.environ.get('URL_K8S_SUFFIX', '')
# system configuration file
# what camera belongs what section
filename = os.environ.get('FILENAME', 'config.json')
data = {}  # data from config file
sections = {'sections': []}  # all sections
cameras = {'cameras': []}  # all cameras


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    """frontend dashboard without pictures"""
    return render_template('index.html')


@app.route('/status', methods=['GET'])
def health():
    """health check"""
    return Response('CPanel ' + version + ' : Online',
                    mimetype='text/plain',
                    status=200)


@app.route('/analysis', methods=['GET'])
def get_analysis():
    """current frame statistics info"""
    destination = dest_momentum + r'/analysis'
    app.logger.debug('momentum url for analysis: ' + destination)
    try:
        response = requests.get(destination)
    except:
        app.logger.error('Failed to reach [' + destination + ']')
        return Response('', status=400)
    return Response(response.json,
                    status=response.status_code)


@app.route('/alert', methods=['GET'])
def get_current_alert():
    """current frame statistics info"""
    destination = dest_momentum + r'/alert'
    app.logger.debug('momentum url for alert: ' + destination)
    try:
        response = requests.get(destination)
    except:
        app.logger.error('Failed to reach [' + destination + ']')
        return Response('', status=400)
    return Response(response.text,
                    status=response.status_code)


@app.route('/momentum/status', methods=['GET'])
def get_momentum_status():
    """get status of momentum"""
    destination = dest_momentum + '/status'
    try:
        response = requests.get(destination)
    except:
        app.logger.error('Failed to reach [' + destination + ']')
        return Response('', status=400)
    app.logger.debug('forwarding GET to momentum: '
                     + destination)
    return Response(response.text,
                    status=response.status_code)


@app.route('/collector/status',
           methods=['GET'])
def get_collector_status():
    """get status of collector"""
    destination = dest_collector + '/status'
    try:
        response = requests.get(destination)
    except:
        app.logger.error('Failed to reach [' + destination + ']')
        return Response('', status=400)
    app.logger.debug('forwarding GET to collector: '
                     + destination)
    return Response(response.text,
                    status=response.status_code)


@app.route('/config',
           methods=['PUT'])
def reload_config():
    """reload config after changes made"""
    app.logger.debug('system config reloaded')
    global data
    global cameras
    global sections
    data = {}
    cameras = {'cameras': []}
    sections = {'sections': []}
    open_file()
    return Response("Config reloaded successful",
                    status=200)


@app.route('/cameras',
           methods=['GET'])
def get_cameras():
    """list of all cameras in system"""
    temp = {'cameras': []}
    for c in cameras['cameras']:
        cam = {}
        cam['id'] = c['id']
        cam['type'] = c['type']
        cam['section'] = c['section']
        temp.get('cameras').append(cam)
    return Response(json.dumps(temp, indent=2),
                    status=200)


@app.route('/cameras/<id>/state',
           methods=['GET'])
def get_state(id):
    """state of camera #id"""
    destination = get_cam_url(id) + r'/state'
    app.logger.debug('camera url: ' + destination)
    app.logger.debug('get state of camera agent: ' + str(id))
    try:
        response = requests.get(destination)
    except:
        app.logger.error('Failed to reach [' + destination + ']')
        return Response('', status=400)
    return Response(response.text,
                    status=response.status_code)


@app.route('/cameras/<id>/stream',
           methods=['POST'])
def start_stream(id):
    """start stream for camera #id"""
    if (request.is_json == True):
        destination = get_cam_url(id) + r'/stream'
        app.logger.debug('start stream on: ' + destination)
        try:
            response = requests.post(destination,
                                     json=request.json,
                                     params=request.args)
        except:
            app.logger.error('Failed to reach [' + destination + ']')
            return Response('', status=400)
        app.logger.info('started camera agent: ' + str(id))
    else:
        return Response('', status=400)
    return Response(response.text,
                    status=response.status_code)


@app.route('/cameras/<id>/frame',
           methods=['GET'])
def get_frame(id):
    """get one frame from camera #id"""
    destination = get_cam_url(id) + r'/frame'
    app.logger.debug('get frame from: ' + destination)
    app.logger.info('get frame from camera agent: ' + str(id))
    try:
        response = requests.get(destination)
    except:
        app.logger.error('Failed to reach [' + destination + ']')
        return Response('', status=400)
    return Response(response.text,
                    status=response.status_code)


@app.route('/sections/<id>/status',
           methods=['GET'])
def get_section_status(id):
    """get status of section"""
    destination = get_section_url(id) + '/status'
    app.logger.debug('forwarding GET to section: '
                     + destination)
    try:
        response = requests.get(destination)
    except:
        app.logger.error('Failed to reach [' + destination + ']')
        return Response('', status=400)
    return Response(response.text,
                    status=response.status_code)


@app.route('/sections',
           methods=['GET'])
def get_sections():
    """list all sections in system from internal config file"""
    temp = {'sections': []}
    for c in sections['sections']:
        cam = {}
        cam['id'] = c['id']
        cam['description'] = c['description']
        temp.get('sections').append(cam)
    return Response(json.dumps(temp, indent=2),
                    status=200)


@app.route('/sections/<id>/persons',
           methods=['POST'])
def save_persons(id):
    """save analyzed persons in section #id"""
    if (request.is_json == True):
        destination = get_section_url(id) + r'/persons'
        app.logger.debug('forward post to: ' + destination)
        app.logger.info('save persons in section: ' + str(id))
        try:
            response = requests.post(destination,
                                     json=request.json)
        except:
            app.logger.error('Failed to reach [' + destination + ']')
            return Response('', status=400)
    else:
        return Response('', status=400)
    return Response(response.text,
                    status=response.status_code)


@app.route('/sections/<id>/persons',
           methods=['GET'])
def filter_persons(id):
    """filter persons in section #id by parameters"""
    destination = get_section_url(id) + r'/persons'
    app.logger.info('filter persons from section: ' + str(id))
    app.logger.debug('forward get to section: ' + destination)
    try:
        response = requests.get(destination,
                                params=request.args)
    except:
        app.logger.error('Failed to reach [' + destination + ']')
        return Response('', status=400)
    return Response(response.text,
                    status=response.status_code)


@app.route('/alerts/',
           methods=['POST'])
def save_alerts():
    """save new alert"""
    if (request.is_json == True):
        app.logger.debug('save alerts from recognition: ')
        destination = dest_alerts + '/'
        try:
            response = requests.post(destination,
                                     json=request.json)
        except:
            app.logger.error('Failed to reach [' + destination + ']')
            return Response('', status=400)
    else:
        return Response('', status=400)
    return Response(response.text,
                    status=response.status_code)


@app.route('/alerts/',
           methods=['GET'])
def filter_alerts():
    """list alerts by parameters"""
    destination = dest_alerts + '/'
    app.logger.debug('filter alerts: ' + destination)
    try:
        response = requests.get(destination,
                                params=request.args)
    except:
        app.logger.error('Failed to reach [' + destination + ']')
        return Response('', status=400)
    return Response(response.text,
                    status=response.status_code)


@app.route('/alerts/status',
           methods=['GET'])
def get_alerts_status():
    """get status of alerts"""
    destination = dest_alerts + '/status'
    app.logger.debug('forwarding GET to alerts: ' + destination)
    try:
        response = requests.get(destination)
    except:
        app.logger.error('Failed to reach [' + destination + ']')
        return Response('', status=400)
    return Response(response.text,
                    status=response.status_code)


@app.route('/alerts/<id>',
           methods=['GET'])
def get_alert(id):
    """get alert by id"""
    destination = dest_alerts + '/' + str(id)
    app.logger.debug('get alert from: ' + destination)
    app.logger.info('get alert by id: ' + str(id))
    try:
        response = requests.get(destination)
    except:
        app.logger.error('Failed to reach [' + destination + ']')
        return Response('', status=400)
    return Response(response.text,
                    status=response.status_code)


@app.route('/alerts/<id>',
           methods=['DELETE'])
def delete_alert(id):
    """delete alert by id"""
    destination = dest_alerts + '/' + str(id)
    app.logger.info('delete alert by id: ' + str(id))
    app.logger.debug('delete alert from: ' + destination)
    try:
        response = requests.delete(destination)
    except:
        app.logger.error('Failed to reach [' + destination + ']')
        return Response('', status=400)
    return Response(response.text,
                    status=response.status_code)


def get_cam_url(id):
    """get url to forward request to proper camera agent"""
    app.logger.info('get camera url by id: ' + str(id))
    for c in cameras['cameras']:
        if c['id'] == int(id):
            url = c['url'] #http://camera-agent-2:8080
            host = url[:-5]
            port = url[-4:]
            app.logger.debug('camera url: ' + host + k8s_suffix + ':' + port)
            return host + k8s_suffix + ':' + port


def get_section_url(id):
    """get url to forward request to proper section"""
    app.logger.debug('get section url')
    for c in sections['sections']:
        if c['id'] == int(id):
            return c['url']


def open_file():
    """read config file of the system"""
    global data
    global cameras
    global sections
    # open data file if exists
    file = pathlib.Path(filename)
    if file.exists():
        app.logger.debug('data file exists')
        with open(filename, 'r', newline='') as file:
            try:
                app.logger.debug('start loading config')
                data = json.load(file)
                app.logger.debug('data file loaded')
            except Exception as e:
                app.logger.error("got %s on json.load()" % e)
    else:
        app.logger.debug('data file does not exist')
    # read all cameras from config
    for cam in data.get('cameras'):
        del cam['description']
        cameras['cameras'].append(cam)
    # read all sections from config
    sections['sections'] = data.get('sections')


@app.route('/production',
           methods=['GET'])
def toggle():
    """start/stop all cameras to stream"""
    param = request.args
    app.logger.debug('start/stop system')
    json_body = []

    for i in cameras['cameras']:
        temp = {}
        temp['section'] = i['section']
        temp['event'] = i['type']
        temp['destination'] = dest_collector
        json_body.append(temp)

    if param.get('toggle') == 'on' or len(request.args) == 0:
        app.logger.debug('send on to camera agents: ')
        for id in range(len(cameras['cameras'])):
            destination = get_cam_url(id+1) + r'/stream'
            try:
                requests.post(destination,
                              json=json_body[id])
            except:
                app.logger.error('Failed to reach [' + destination + ']')
                return Response('', status=400)
        headers = [{'Access-Control-Allow-Origin', '*'}]
        return Response('',
                        status=200,
                        headers=headers)
    elif param.get('toggle') == 'off':
        app.logger.info('send off to camera agents: ')
        for id in range(len(cameras['cameras'])):
            destination = get_cam_url(id+1) + r'/stream?toggle=off'
            try:
                requests.post(destination,
                              json=json_body[id])
            except:
                app.logger.error('Failed to reach [' + destination + ']')
                return Response('', status=400)
        headers = [{'Access-Control-Allow-Origin', '*'}]
        return Response('',
                        status=200,
                        headers=headers)
    return Response('', status=400)


if __name__ == '__main__':
    open_file()  # read config on server start
    app.run(host=bind_to['hostname'], port=int(bind_to['port']), debug=True)
