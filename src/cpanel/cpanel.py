from flask import Flask, request, abort, Response
import requests
import json
import pathlib
import logging


app = Flask(__name__)

bind_to = {'hostname': "0.0.0.0", 'port': 8080}
# system configuration file
# what camera belongs what section
filename = 'config.json'
data = {}  # data from config file
sections = {'sections': []}  # all sections
cameras = {'cameras': []}  # all cameras
dest_alerts = ''  # where to send alerts


@app.route('/status', methods=['GET'])
def show_status():
    return Response("CPanel : Online", status=200, mimetype="text/plain")


@app.route('/config', methods=['PUT'])
def reload_config():
    """endpoint to reload config after changes made"""
    app.logger.debug('reload system config')
    global data
    global cameras
    global sections
    data = {}
    cameras = {'cameras': []}
    sections = {'sections': []}
    open_file()
    return Response("Config reloaded successful", status=200)


@app.route('/cameras', methods=['GET'])
def get_cameras():
    """list of all cameras in system"""
    temp = {'cameras': []}
    for c in cameras['cameras']:
        cam = {}
        cam['id'] = c['id']
        cam['type'] = c['type']
        cam['section'] = c['section']
        temp.get('cameras').append(cam)
    return Response(json.dumps(temp, indent=2), status=200)


@app.route('/cameras/<id>/state', methods=['GET'])
def get_state(id):
    """state of camera #id"""
    response = requests.get(get_cam_url(id)+r'/state')
    app.logger.debug('get state of camera agent: ' + str(id))
    return Response(response.text, status=response.status_code)


@app.route('/cameras/<id>/stream', methods=['POST'])
def start_stream(id):
    """start stream for camera #id"""
    if (request.is_json == True):
        print(get_cam_url(id)+r'/stream')
        response = requests.post(get_cam_url(
            id)+r'/stream', json=request.json, params=request.args)
        print('start camera agent: ' + str(id))
    else:
        return abort(400)
    return Response(response.text, status=response.status_code)


@app.route('/cameras/<id>/frame', methods=['GET'])
def get_frame(id):
    """get one frame from camera #id"""
    response = requests.get(get_cam_url(id)+r'/frame')
    app.logger.debug('frame from camera agent: ' + str(id))
    return Response(response.text, status=response.status_code)


@app.route('/sections', methods=['GET'])
def get_sections():
    """list all sections in system"""
    temp = {'sections': []}
    for c in sections['sections']:
        cam = {}
        cam['id'] = c['id']
        cam['description'] = c['description']
        temp.get('sections').append(cam)
    return Response(json.dumps(temp, indent=2), status=200)


@app.route('/sections/<id>/persons', methods=['POST'])
def save_persons(id):
    """save analyzed persons in section #id"""
    if (request.is_json == True):
        app.logger.debug('save persons in section: ' + str(id))
        response = requests.post(get_section_url(
            id)+r'/persons', json=request.json)
    else:
        return abort(400)
    return Response(response.text, status=response.status_code)


@app.route('/sections/<id>/persons', methods=['GET'])
def filter_persons(id):
    """filter persons in section #id by parameters"""
    response = requests.get(get_section_url(
        id)+r'/persons', params=request.args)
    app.logger.debug('persons from section: ' + str(id))
    return Response(response.text, status=response.status_code)


@app.route('/alerts/', methods=['POST'])
def save_alerts():
    """save new alert"""
    if (request.is_json == True):
        app.logger.debug('save alerts from recognition: ')
        response = requests.post(dest_alerts + '/', json=request.json)
    else:
        return abort(400)
    return Response(response.text, status=response.status_code)


@app.route('/alerts/', methods=['GET'])
def filter_alerts():
    """list alerts by parameters"""
    response = requests.get(dest_alerts + '/', params=request.args)
    app.logger.debug('filter alerts: ')
    return Response(response.text, status=response.status_code)


@app.route('/alerts/<id>', methods=['GET'])
def get_alert(id):
    """get alert by id"""
    app.logger.debug('get alert by id: ' + str(id))
    response = requests.get(dest_alerts + '/' + str(id))
    app.logger.debug('get alert by id: ' + str(id))
    return Response(response.text, status=response.status_code)


@app.route('/alerts/<id>', methods=['DELETE'])
def delete_alert(id):
    """delete alert by id"""
    app.logger.debug(dest_alerts + '/' + str(id))
    response = requests.delete(dest_alerts + '/' + str(id))
    app.logger.debug('delete alert by id: ' + str(id))
    return Response(response.text, status=response.status_code)


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
    global dest_alerts
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
    dest_alerts = data.get('alerts').get('url')


@app.route('/system', methods=['POST'])
def toggle():
    """start all cameras to stream"""
    param = request.args
    app.logger.debug('start system')
    json_body = []

    for i in cameras['cameras']:
        temp = {}
        temp['section'] = i['section']
        temp['event'] = i['type']
        temp['destination'] = data['collector']['url']
        json_body.append(temp)

    if param.get('toggle') == 'on' or len(request.args) == 0:
        for id in range(len(cameras['cameras'])):
            app.logger.debug('send on to camera: ')
            response = requests.post(get_cam_url(
                id+1)+r'/stream', json=json_body[id])
        return Response('', status=200)
    elif param.get('toggle') == 'off':
        for id in range(len(cameras['cameras'])):
            app.logger.debug('send on to camera: ')
            response = requests.post(get_cam_url(
                id+1)+r'/stream?toggle=off', json=json_body[id])
        return Response('', status=200)
    return abort(400)


if __name__ == '__main__':
    open_file()  # read config on server start
    app.run(host=bind_to['hostname'], port=int(bind_to['port']), debug=True)
