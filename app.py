from flask import Flask, request
import flask
import requests
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
# CORS(app)
# socketio = SocketIO(app)

@app.route('/', methods=['POST'])
def parse_request():
    data = request.data  # data is empty
    # need posted data here
    print(data)
    os.system("python3 Sparql.py "+str(data))


    f = open("out", "r")
    line = f.read()
    f.close()
    print(line)
    result = {"value": line,"type": "value"}
    result = json.dumps(result)
    resp = flask.Response(result)
    print("result: "+result)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(host= '0.0.0.0', port=8000)
