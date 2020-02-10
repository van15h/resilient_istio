from flask import Flask, request, abort, Response
import requests
import json
import pathlib
import logging
from datetime import datetime
import os


app = Flask(__name__)

port = int(os.environ.get('PORT', 8080))
bind_to = {'hostname': '0.0.0.0', 'port': port}
# read envirenment variable to determine section id
filename = 'data_persons_' + os.environ['SECTION'] + '.json'


@app.route('/status', methods=['GET'])
def show_status():
    return Response("Section " + os.environ['SECTION'] + " : Online", status=200, mimetype="text/plain")


@app.route('/persons', methods=['POST'])
def send_persons():
    """post forwarded from face recognition"""
    app.logger.debug('post from face collector')
    if (request.is_json == True):
        app.logger.debug('is json')
        return process(request.json)
    else:
        return abort(400)


@app.route('/persons', methods=['GET'])
def get_persons():
    """filter persons by parameters"""
    num = len(request.args)
    app.logger.debug('get persons with ' + str(num) + ' parameters')
    if num == 0 or num == 1 or num == 2 or num > 4:
        return abort(400)
    return filter_stats(request.args)


def filter_stats(obj):
    """filter persons by provided arguments"""
    aggr = ''
    departed = ''
    # parse request params
    try:
        t1 = datetime.strptime(obj.get('from'), '%Y-%m-%dT%H:%M:%S.%f%z')
        t2 = datetime.strptime(obj.get('to'), '%Y-%m-%dT%H:%M:%S.%f%z')
    except Exception as e:
        return Response(str(e), status=400)
    # print(type(t2))
    if 'aggregate' in obj:
        if (str(obj.get('aggregate')) == 'count'):
            aggr = 'count'
        else:
            return abort(400)
    if 'departed' in obj:
        if (str(obj.get('departed')) == 'true'):
            departed = 'exit'
        elif (str(obj.get('departed')) == 'false'):
            departed = 'entry'
        else:
            return abort(400)
    app.logger.debug('request checked on parameters')
    # read data file
    data = []
    file = pathlib.Path(filename)
    if file.exists():
        app.logger.debug('data file exists')
        with open(filename) as json_file:
            try:
                data = json.load(json_file)
                app.logger.debug('data file loaded')
            except Exception as e:
                app.logger.debug('got %s on json.load()' % e)
    else:
        app.logger.debug('data file does not exist')
    # filter data
    response = []
    number_of_persons = 0
    if len(obj) == 4:
        app.logger.debug('start processing 4 parameters')
        for pers_data in data:
            for pers in pers_data['persons']:
                if (pers['event'] == departed) and (aggr == 'count') and(t1 <= datetime.strptime(pers['timestamp'], '%Y-%m-%dT%H:%M:%S.%f%z') <= t2):
                    number_of_persons += 1
        app.logger.debug('found people: ' + str(number_of_persons))
    else:
        if aggr == '':
            app.logger.debug('start processing 3 parameters without aggr')
            for pers_data in data:
                for pers in pers_data['persons']:
                    if (pers['event'] == departed) and (t1 <= datetime.strptime(pers['timestamp'], '%Y-%m-%dT%H:%M:%S.%f%z') <= t2):
                        response.append(pers)
        else:
            app.logger.debug('start processing 3 parameters aggregated')
            for pers_data in data:
                for pers in pers_data['persons']:
                    if t1 <= datetime.strptime(pers['timestamp'], '%Y-%m-%dT%H:%M:%S.%f%z') <= t2:
                        number_of_persons += 1
    if aggr == '':
        return Response(json.dumps(response, indent=2), status=200)
    else:
        return Response(str(number_of_persons), status=200)


def process(obj):
    """save persons in db file"""
    data = []
    file = pathlib.Path(filename)
    if file.exists():
        app.logger.debug('data file exists')
        with open(filename) as json_file:
            try:
                data = json.load(json_file)
                app.logger.debug('data file loaded')
            except Exception as e:
                app.logger.debug('got %s on json.load()' % e)
                return abort(400)
    else:
        app.logger.debug('data file does not exist')
    data.append(obj)
    app.logger.debug('data file added new persons')
    # save data
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=2)
        app.logger.debug('data file saved')
    return Response('', status=200)


if __name__ == '__main__':
    app.run(host=bind_to['hostname'], port=int(bind_to['port']), debug=True)
