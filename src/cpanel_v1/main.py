from flask import Flask, request, Response, render_template
import requests
import json
import pathlib
import logging
import os
import time

app = Flask(__name__)

port = int(os.environ.get('PORT', 8080))
bind_to = {'hostname': '0.0.0.0',
           'port': port}
version = os.environ.get('VERSION', 'v1')
dest_alerts = os.environ.get('URL_ALERTS',
                             'http://alerts:8080')
dest_collector = os.environ.get('URL_COLLECTOR',
                                'http://collector:8080')
# system configuration file
# what camera belongs what section
filename = os.environ.get('FILENAME',
                          'config.json')
data = {}  # data from config file
sections = {'sections': []}  # all sections
cameras = {'cameras': []}  # all cameras
stats_analysis = {'persons': [
    {
        'age': 'empty',
        'gender': 'empty',
        'event': 'empty',
        'timestamp': 'empty'
    },
]}
stats_alert = {}


@app.route('/',
           methods=['GET'])
@app.route('/index',
           methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/status',
           methods=['GET'])
def show_status():
    return Response('CPanel ' + version + ' : Online',
                    mimetype='text/plain',
                    status=200)


@app.route('/analysis',
           methods=['GET'])
def get_analysis():
    return Response(json.dumps(stats_analysis, indent=2),
                    status=200)


@app.route('/alert',
           methods=['GET'])
def get_current_alert():
    return Response(json.dumps(stats_alert, indent=2),
                    status=200)


@app.route('/analysis',
           methods=['POST'])
def post_analysis():
    global stats_analysis
    if (request.is_json == True):
        app.logger.debug('got statistic from analysis')
        app.logger.debug('analysis timestamp:'
                         + str(request.json['timestamp']))
        stats_analysis = request.json
    else:
        return Response('', status=400)
    return Response('', status=200)


@app.route('/alert',
           methods=['POST'])
def post_alert():
    global stats_alert
    if (request.is_json == True):
        app.logger.debug('got alert from face recognition')
        app.logger.debug('alert timestamp: '
                         + request.json['timestamp'])
        stats_alert = request.json
    else:
        return Response('', status=400)
    return Response('', status=200)


@app.route('/collector/status',
           methods=['GET'])
def get_collector_status():
    """get status of collector"""
    status_url = dest_collector + '/status'
    response = requests.get(status_url)
    app.logger.debug('forwarding GET to collector: '
                     + status_url)
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
    response = requests.get(get_cam_url(id)
                            + r'/state')
    app.logger.debug('camera url: '
                     + get_cam_url(id)
                     + r'/state')
    app.logger.debug('get state of camera agent: '
                     + str(id))
    return Response(response.text,
                    status=response.status_code)


@app.route('/cameras/<id>/stream',
           methods=['POST'])
def start_stream(id):
    """start stream for camera #id"""
    if (request.is_json == True):
        app.logger.debug(get_cam_url(id)
                         + r'/stream')
        response = requests.post(get_cam_url(id)
                                 + r'/stream',
                                 json=request.json,
                                 params=request.args)
        app.logger.debug('start camera agent: '
                         + str(id))
    else:
        return Response('', status=400)
    return Response(response.text,
                    status=response.status_code)


@app.route('/cameras/<id>/frame',
           methods=['GET'])
def get_frame(id):
    """get one frame from camera #id"""
    response = requests.get(get_cam_url(id)
                            + r'/frame')
    app.logger.debug('frame from camera agent: '
                     + str(id))
    return Response(response.text,
                    status=response.status_code)


@app.route('/sections/<id>/status',
           methods=['GET'])
def get_section_status(id):
    """get status of section"""
    status_url = get_section_url(id) + '/status'
    app.logger.debug('forwarding GET to section: '
                     + status_url)
    response = requests.get(status_url)
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
        app.logger.debug('save persons in section: '
                         + str(id))
        response = requests.post(get_section_url(id)
                                 + r'/persons',
                                 json=request.json)
    else:
        return Response('', status=400)
    return Response(response.text,
                    status=response.status_code)


@app.route('/sections/<id>/persons',
           methods=['GET'])
def filter_persons(id):
    """filter persons in section #id by parameters"""
    response = requests.get(get_section_url(id)
                            + r'/persons',
                            params=request.args)
    app.logger.debug('persons from section: '
                     + str(id))
    return Response(response.text,
                    status=response.status_code)


@app.route('/alerts/',
           methods=['POST'])
def save_alerts():
    """save new alert"""
    if (request.is_json == True):
        app.logger.debug('save alerts from recognition: ')
        response = requests.post(dest_alerts + '/',
                                 json=request.json)
    else:
        return Response('', status=400)
    return Response(response.text,
                    status=response.status_code)


@app.route('/alerts/',
           methods=['GET'])
def filter_alerts():
    """list alerts by parameters"""
    request_url = dest_alerts + '/'
    response = requests.get(request_url,
                            params=request.args)
    app.logger.debug('filter alerts: '
                     + request_url)
    return Response(response.text,
                    status=response.status_code)


@app.route('/alerts/status',
           methods=['GET'])
def get_alerts_status():
    """get status of alerts"""
    status_url = dest_alerts + '/status'
    response = requests.get(status_url)
    app.logger.debug('forwarding GET to alerts: '
                     + status_url)
    return Response(response.text,
                    status=response.status_code)


@app.route('/alerts/<id>',
           methods=['GET'])
def get_alert(id):
    """get alert by id"""
    app.logger.debug('get alert by id: ' + str(id))
    response = requests.get(dest_alerts + '/' + str(id))
    app.logger.debug('get alert by id: ' + str(id))
    return Response(response.text,
                    status=response.status_code)


@app.route('/alerts/<id>',
           methods=['DELETE'])
def delete_alert(id):
    """delete alert by id"""
    app.logger.debug(dest_alerts + '/' + str(id))
    response = requests.delete(dest_alerts + '/' + str(id))
    app.logger.debug('delete alert by id: ' + str(id))
    return Response(response.text,
                    status=response.status_code)


def get_cam_url(id):
    """get url to forward request to proper camera agent"""
    app.logger.debug('get camera url')
    for c in cameras['cameras']:
        if c['id'] == int(id):
            return c['url']


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
        print('data file exists')
        with open(filename, 'r', newline='') as file:
            try:
                print('start loading config')
                data = json.load(file)
                print('data file loaded')
            except Exception as e:
                print("got %s on json.load()" % e)
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
            requests.post(get_cam_url(id+1)
                          + r'/stream',
                          json=json_body[id])
        headers = [{'Access-Control-Allow-Origin', '*'}]
        return Response('',
                        status=200,
                        headers=headers)
    elif param.get('toggle') == 'off':
        app.logger.debug('send off to camera agents: ')
        for id in range(len(cameras['cameras'])):
            requests.post(get_cam_url(id+1)
                          + r'/stream?toggle=off',
                          json=json_body[id])
        headers = [{'Access-Control-Allow-Origin', '*'}]
        return Response('',
                        status=200,
                        headers=headers)
    return Response('', status=400)


if __name__ == '__main__':
    open_file()  # read config on server start
    app.run(host=bind_to['hostname'], port=int(bind_to['port']), debug=True)
