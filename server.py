import hashlib
import hmac
import json
import logging
import os
import time
import urllib.parse

import requests

from flask import Flask, request
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

config = {
    'signing_secret': os.environ.get('SIGNING_SECRET'),
    'target_webhook': os.environ.get('TARGET_WEBHOOK'),
    'options': {
        'default': {
            'username':
            'Abakus',
            'icon_url':
            'https://avatars2.githubusercontent.com/u/10448101?s=200&v=4'
        }
    }
}


def legal_config():
    return config['signing_secret'] is not None and config[
        'target_webhook'] is not None


def validate_request(signature, timestamp, request_body):
    if abs(time.time() - float(timestamp)) > 60 * 5:
        return False, 'Old request'
    basestring = f"v0:{timestamp}:{request_body}".encode('utf-8')
    computed_signature = 'v0=' + hmac.new(
        bytes(config['signing_secret'], 'utf-8'), basestring,
        hashlib.sha256).hexdigest()
    if not hmac.compare_digest(computed_signature, signature):
        return False, "Signature didn't match"
    return True, None


def handle_action(body):
    r = requests.post(
        config['target_webhook'],
        data=json.dumps({
            **config['options']['default'], 'text':
            body['message']['text']
        }))


@app.before_request
def fix_transfer_encoding():
    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == u"chunked":
        request.environ["wsgi.input_terminated"] = True


@app.route("/", defaults={"path": ""}, methods=["GET"])
def main_route(path):
    return json.dumps({
        'signing_secret': config['signing_secret'] is not None,
        'target_webhook': config['target_webhook'] is not None
    }), 200


@app.route("/", defaults={"path": ""}, methods=["POST"])
def action_route(path):
    print("yeet")
    if not legal_config():
        return 'Not configured right', 400
    slack_signature = request.headers['X-Slack-Signature']
    timestamp = request.headers['X-Slack-Request-Timestamp']
    request_body = request.get_data().decode('utf-8')
    ok, err = validate_request(slack_signature, timestamp, request_body)
    if not ok:
        return err, 400
    # raise Exception(urllib.parse.unquote_plus(request_body[8:]))
    request_body = urllib.parse.unquote_plus(request_body[8:])
    handle_action(json.loads(request_body))

    return '', 200


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
