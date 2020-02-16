from flask import Flask, request, abort, Response
import requests
import json
import pathlib
from datetime import datetime
import logging
import os


app = Flask(__name__)

port = int(os.environ.get('PORT', 8080))
bind_to = {'hostname': '0.0.0.0',
           'port': port}
# db file to save alerts
filename = os.environ.get('FILENAME',
                          'data_alerts.json')
dest_cpanel = os.environ.get('URL_CPANEL',
                             'http://cpanel:8080/alert')


@app.route('/status',
           methods=['GET'])
def show_status():
    return Response('Alerts : Online',
                    mimetype='text/plain',
                    status=200)


@app.route('/',
           methods=['GET'])
def filter():
    """filter alerts depending on parameters"""
    if len(request.args) == 0:
        app.logger.debug('get all alerts by id')
        return Response(json.dumps(open_file()),
                        status=200)
    app.logger.debug('get list filtered alerts')
    return filter_alerts(request.args)


@app.route('/',
           methods=['POST'])
def send_alert():
    """save alert in db file"""
    app.logger.debug('post from face recognition')
    if request.is_json == True:
        app.logger.debug('is json')
        forward_cpanel(request.json)
        process(request.json)
    else:
        return Response('', status=400)
    return Response('', status=200)


@app.route('/<id>',
           methods=['GET'])
def get_alert(id):
    """get alert by id"""
    app.logger.debug('get person by id')
    return get_details(id)


@app.route('/<id>',
           methods=['DELETE'])
def delete_alert(id):
    """delete alert by id"""
    app.logger.debug('delete person by id')
    return delete(id)


def forward_cpanel(obj):
    try:
        requests.post(dest_cpanel,
                      json=obj)
    except:
        app.logger.error('Failed to reach [' + dest_cpanel + ']')
        return Response('', status=400)


def filter_alerts(obj):
    """filter alerts by parameters"""
    aggr = ''
    # parse request params
    try:
        t1 = datetime.strptime(obj.get('from'),
                               '%Y-%m-%dT%H:%M:%S.%f%z')
        t2 = datetime.strptime(obj.get('to'),
                               '%Y-%m-%dT%H:%M:%S.%f%z')
    except Exception as e:
        return Response(str(e),
                        status=400)
    if 'aggregate' in obj:
        if (str(obj.get('aggregate')) == 'count'):
            aggr = 'count'
        else:
            return Response('should be agreggate=count',
                            status=400)
    data = open_file()
    response = []
    number_of_persons = 0
    if aggr == '':
        app.logger.debug('start processing 3 parameters without aggr')
        for alert in data:
            if t1 <= datetime.strptime(alert['timestamp'],
                                       '%Y-%m-%dT%H:%M:%S.%f%z') <= t2:
                response.append(alert)
    else:
        app.logger.debug('start processing 3 parameters aggregated')
        for alert in data:
            if t1 <= datetime.strptime(alert['timestamp'],
                                       '%Y-%m-%dT%H:%M:%S.%f%z') <= t2:
                number_of_persons += 1
    if aggr == '':
        return Response(json.dumps(response, indent=2),
                        status=200)
    else:
        return Response(str(number_of_persons),
                        status=200)


def delete(id):
    """delete alert by id"""
    data = open_file()
    app.logger.debug('total of alerts: '
                     + str(len(data)))
    # process request
    app.logger.debug('search for id in data')
    for alert in data:
        if str(alert['id']) == str(id):
            app.logger.debug('id found')
            data.remove(alert)
            app.logger.debug('alert deleted')
            # save data
            with open(filename, 'w') as json_file:
                json.dump(data,
                          json_file,
                          indent=2)
                app.logger.debug('data file saved')
            return Response('', status=200)
    return Response('', status=404)


def get_details(id):
    """get alert by id"""
    data = open_file()
    app.logger.debug('total of alerts: '
                     + str(len(data)))
    # process request
    app.logger.debug('search for id in data')
    for alert in data:
        if str(alert['id']) == str(id):
            app.logger.debug('id found')
            return Response(json.dumps(alert, indent=2),
                            status=200)
    return Response('', status=404)


def process(obj):
    """save alert to db file"""
    counter = 0
    data = open_file()
    if len(data) == 1:
        counter = data[0]['id']
    elif len(data) > 1:
        counter = data[-1]['id']
    app.logger.debug('counter = ' + str(counter))
    counter += 1
    # data processing
    del obj['image']
    obj['id'] = counter
    data.append(obj)
    app.logger.debug('data file added new persons')
    # save data
    with open(filename, 'w') as json_file:
        json.dump(data,
                  json_file,
                  indent=2)
        app.logger.debug('data file saved')
    return Response("", status=200)


def open_file():
    """open db file"""
    # open data file if exists
    file = pathlib.Path(filename)
    if file.exists():
        app.logger.debug('data file exists')
        with open(filename) as json_file:
            try:
                return json.load(json_file)
                app.logger.debug('data file loaded')
            except Exception as e:
                app.logger.debug("got %s on json.load()" % e)
    else:
        app.logger.debug('data file does not exist')
        return []


if __name__ == '__main__':
    app.run(host=bind_to['hostname'], port=int(bind_to['port']), debug=True)
