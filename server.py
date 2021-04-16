import hashlib
import hmac
import json
import logging
import sys
import time
import urllib.parse

import requests
from flask import Flask, request
from gevent.pywsgi import WSGIServer

from config import config, legal_config

app = Flask(__name__)


class ValidationException(Exception):
    pass


def validate_request(signature, timestamp, request_body):
    if abs(time.time() - float(timestamp)) > 60 * 5:
        raise ValidationException("Request too old")
    basestring = f"v0:{timestamp}:{request_body}".encode("utf-8")
    computed_signature = (
        "v0="
        + hmac.new(
            bytes(config["signing_secret"], "utf-8"), basestring, hashlib.sha256
        ).hexdigest()
    )

    if not hmac.compare_digest(computed_signature, signature):
        raise ValidationException("Signature didn't match")


def post_json(url, body):
    return requests.post(
        url, json=body, headers={"Authorization": f'Bearer {config["oauth_token"]}'}
    )


def publish_message(body):
    r = requests.post(
        config["target_webhook"],
        data=json.dumps(
            {
                **config["options"]["default"],
                **config["options"][body["submission"]["post_as"]],
                "text": body["submission"]["message"],
                "channel": body["submission"]["channel"],
            }
        ),
    )

    if r.status_code == 200:
        print(
            f'{body["user"]["name"]} posted a message as {body["submission"]["post_as"]} to {body["submission"]["channel"]}'
        )
    else:
        raise Exception(
            f'{body["user"]["name"]} was unable to post to {body["submission"]["channel"]}'
        )


def handle_action(body):
    print(f'Handeling {body["type"]} request from {body["user"]["name"]}')

    if body["channel"]["id"] != config["channel_id"]:
        post_json(
            body["response_url"],
            {
                "text": "Du kan ikke poste fra denne kanalen :(",
                "response_type": "ephemeral",
            },
        )
    elif body["callback_id"] == "x_publish" and body["type"] == "message_action":
        open_dialog(body)
    elif body["callback_id"] == "x_publish" and body["type"] == "dialog_submission":
        publish_message(body)
    else:
        raise Exception("Action type not recognized")


def open_dialog(body):
    post_json(
        "https://slack.com/api/dialog.open", config["dialogs"]["post_message"](body)
    )


@app.before_request
def fix_transfer_encoding():
    transfer_encoding = request.headers.get("Transfer-Encoding", None)

    if transfer_encoding == "chunked":
        request.environ["wsgi.input_terminated"] = True


@app.after_request
def flush_streams(response):
    sys.stdout.flush()
    sys.stderr.flush()

    return response


@app.route("/", defaults={"path": ""}, methods=["GET"])
def main_route(path):
    return (
        json.dumps(
            {
                "ok": legal_config(),
            }
        ),
        200,
    )


@app.route("/", defaults={"path": ""}, methods=["POST"])
def action_route(path):
    if not legal_config():
        return "", 400
    try:
        slack_signature = request.headers["X-Slack-Signature"]
        timestamp = request.headers["X-Slack-Request-Timestamp"]
        request_body = request.get_data().decode("utf-8")
        validate_request(slack_signature, timestamp, request_body)

        request_body = json.loads(urllib.parse.unquote_plus(request_body[8:]))
        handle_action(request_body)
    except Exception as e:
        print(f"Exception during handle: {str(e)}")
        logging.exception("Error Stack")

        return "", 400

    return "", 200


if __name__ == "__main__":
    http_server = WSGIServer(("", 5000), app)
    http_server.serve_forever()
