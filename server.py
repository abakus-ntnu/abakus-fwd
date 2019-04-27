import hashlib
import hmac
import json
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
    'oauth_token': os.environ.get('OAUTH_TOKEN'),
    'options': {
        'default': {
            'username':
            'Abakus',
            'icon_url':
            'https://avatars2.githubusercontent.com/u/10448101?s=200&v=4'
        },
        'hovedstyret': {
            'username':
            'Hovedstyret',
            'icon_url':
            'https://thumbor.abakus.no/RGmrcG8YoEhhPKWY7suqAcMpaEA=/500x500/hs_ny_kY3AqO8.png'
        }
    },
    'responses': {
        'good': {
            'text': 'Yeet',
            'response_type': 'ephemeral'
        },
        'bad': {
            'text': 'Neet',
            'response_type': 'ephemeral'
        },
    }
}


def legal_config():
    return config['signing_secret'] is not None and config[
        'target_webhook'] is not None and config['oauth_token'] is not None


def validate_request(signature, timestamp, request_body):
    if abs(time.time() - float(timestamp)) > 60 * 5:
        return False, 'Old request'
    basestring = f'v0:{timestamp}:{request_body}'.encode('utf-8')
    computed_signature = 'v0=' + hmac.new(
        bytes(config['signing_secret'], 'utf-8'), basestring,
        hashlib.sha256).hexdigest()
    if not hmac.compare_digest(computed_signature, signature):
        return False, "Signature didn't match"
    return True, None


def post_json(url, body):
    return requests.post(
        url,
        json=body,
        headers={'Authorization': f'Bearer {config["oauth_token"]}'})


def handle_action(body):
    if (body['callback_id'] == 'x-abakus'):
        open_dialog(body)
    elif (body['callback_id'] == 'x-dialog'):
        r = requests.post(
            config['target_webhook'],
            data=json.dumps({
                **config['options']['default'],
                **config['options'][body['submission']['post_as']], 'text':
                body['submission']['message'],
                'channel':
                body['submission']['channel']
            }))
        # if (r.status_code == 200 and r.json()['ok']):
        #     pass
        # else:
        #     pass


def open_dialog(body):
    post_json(
        'https://slack.com/api/dialog.open', {
            'trigger_id': body['trigger_id'],
            'dialog': {
                'callback_id':
                'x-dialog',
                'title':
                'Publiser i Abakus',
                'submit_label':
                'Publiser',
                'elements': [{
                    'type': 'textarea',
                    'label': 'Melding',
                    'name': 'message',
                    'value': body['message']['text']
                },
                             {
                                 'type': 'text',
                                 'label': 'Kanal (typ #general)',
                                 'name': 'channel',
                             },
                             {
                                 'label':
                                 'Post som',
                                 'type':
                                 'select',
                                 'name':
                                 'post_as',
                                 'options': [
                                     {
                                         'label': 'Hovedstyret',
                                         'value': 'hovedstyret'
                                     },
                                 ]
                             }]
            }
        })


@app.before_request
def fix_transfer_encoding():
    transfer_encoding = request.headers.get('Transfer-Encoding', None)
    if transfer_encoding == u'chunked':
        request.environ['wsgi.input_terminated'] = True


@app.route('/', defaults={'path': ''}, methods=['GET'])
def main_route(path):
    return json.dumps({
        'signing_secret': config['signing_secret'] is not None,
        'target_webhook': config['target_webhook'] is not None,
        'oauth_token': config['oauth_token'] is not None
    }), 200


@app.route('/', defaults={'path': ''}, methods=['POST'])
def action_route(path):
    if not legal_config():
        return 'Not configured right', 400
    slack_signature = request.headers['X-Slack-Signature']
    timestamp = request.headers['X-Slack-Request-Timestamp']
    request_body = request.get_data().decode('utf-8')
    ok, err = validate_request(slack_signature, timestamp, request_body)
    if not ok:
        return err, 400
    request_body = json.loads(urllib.parse.unquote_plus(request_body[8:]))
    handle_action(request_body)

    return '', 200


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
