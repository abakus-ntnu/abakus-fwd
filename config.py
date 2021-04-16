import os

BASE_URL = "https://github.com/abakus-ntnu/abakus-fwd/tree/2021/icons/"
OPTIONS = {
    "abakus": {
        "username": "Abakus",
        "icon_url": BASE_URL + "abakule.png",
        "link_names": True,
        "unfurl_links": True,
    },
    "hovedstyret": {
        "username": "Hovedstyret",
        "icon_url": BASE_URL + "hs.png",
        "link_names": True,
        "unfurl_links": True,
    },
    "inter": {
        "username": "INTER",
        "icon_url": BASE_URL + "inter.png",
        "link_names": True,
        "unfurl_links": True,
    },
    "media": {
        "username": "MEDIA",
        "icon_url": BASE_URL + "media.png",
        "link_names": True,
        "unfurl_links": True,
    },
    "sosial": {
        "username": "SOSIAL",
        "icon_url": BASE_URL + "sosial.png",
        "link_names": True,
        "unfurl_links": True,
    },
    "bedriftskontakt": {
        "username": "Bedriftskontakt",
        "icon_url": BASE_URL + "bedkom.png",
        "link_names": True,
        "unfurl_links": True,
    },
    "fondstyret": {
        "username": "Fondstyret",
        "icon_url": BASE_URL + "fondstyret.png",
        "link_names": True,
        "unfurl_links": True,
    },
    "arrkom": {
        "username": "Arrkom",
        "icon_url": BASE_URL + "arrkom.png",
        "link_names": True,
        "unfurl_links": True,
    },
    "backup": {
        "username": "backup",
        "icon_url": BASE_URL + "backup.png",
        "link_names": True,
        "unfurl_links": True,
    },
    "bedkom": {
        "username": "Bedkom",
        "icon_url": BASE_URL + "bedkom.png",
        "link_names": True,
        "unfurl_links": True,
    },
    "fagkom": {
        "username": "Fagkom",
        "icon_url": BASE_URL + "fagkom.png",
        "link_names": True,
        "unfurl_links": True,
    },
    "webkom": {
        "username": "Webkom",
        "icon_url": BASE_URL + "webkom.png",
        "link_names": True,
        "unfurl_links": True,
    },
    "koskom": {
        "username": "Koskom",
        "icon_url": BASE_URL + "koskom.png",
        "link_names": True,
        "unfurl_links": True,
    },
    "labamba": {
        "username": "LaBamba",
        "icon_url": BASE_URL + "labamba.png",
        "link_names": True,
        "unfurl_links": True,
    },
    "pr": {
        "username": "PR",
        "icon_url": BASE_URL + "pr.png",
        "link_names": True,
        "unfurl_links": True,
    },
    "readme": {
        "username": "readme",
        "icon_url": BASE_URL + "readme.png",
        "link_names": True,
        "unfurl_links": True,
    },
    "revy": {
        "username": "Revyen",
        "icon_url": BASE_URL + "revy.png",
        "link_names": True,
        "unfurl_links": True,
    },
}


config = {
    "signing_secret": os.environ.get("SIGNING_SECRET"),
    "target_webhook": os.environ.get("TARGET_WEBHOOK"),
    "oauth_token": os.environ.get("OAUTH_TOKEN"),
    "options": OPTIONS,
    "dialogs": {
        "post_message": lambda body: {
            "trigger_id": body["trigger_id"],
            "dialog": {
                "callback_id": "x_publish",
                "title": "Publiser i Abakus",
                "submit_label": "Publiser",
                "elements": [
                    {
                        "type": "textarea",
                        "label": "Melding",
                        "name": "message",
                        "value": body["message"]["text"],
                    },
                    {
                        "type": "text",
                        "label": "Kanal (typ #general)",
                        "name": "channel",
                    },
                    {
                        "label": "Post som",
                        "type": "select",
                        "name": "post_as",
                        "options": [
                            {
                                "label": v["username"],
                                "value": k,
                            }

                            for (k, v) in OPTIONS.items()
                        ],
                    },
                ],
            },
        }
    },
}


def legal_config():
    return (
        config["signing_secret"] is not None
        and config["target_webhook"] is not None
        and config["oauth_token"] is not None
    )
