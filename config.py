import os


def get_URL(name):
    return (
        "https://github.com/abakus-ntnu/abakus-fwd/blob/master/icons/"
        + name
        + ".png?raw=true"
    )


OPTIONS = {
    "default": {
        "username": "Abakus",
        "icon_url": get_URL("abakule"),
        "link_names": True,
        "unfurl_links": True,
    },
    "hovedstyret": {
        "username": "Hovedstyret",
        "icon_url": get_URL("hs"),
    },
    "inter": {
        "username": "INTER",
        "icon_url": get_URL("inter"),
    },
    "media": {
        "username": "MEDIA",
        "icon_url": get_URL("media"),
    },
    "sosial": {
        "username": "SOSIAL",
        "icon_url": get_URL("sosial"),
    },
    "bedriftskontakt": {
        "username": "Bedriftskontakt",
        "icon_url": get_URL("bedkom"),
    },
    "fondstyret": {
        "username": "Fondstyret",
        "icon_url": get_URL("fondstyret"),
    },
    "arrkom": {
        "username": "Arrkom",
        "icon_url": get_URL("arrkom"),
    },
    "backup": {
        "username": "backup",
        "icon_url": get_URL("backup"),
    },
    "bedkom": {
        "username": "Bedkom",
        "icon_url": get_URL("bedkom"),
    },
    "fagkom": {
        "username": "Fagkom",
        "icon_url": get_URL("fagkom"),
    },
    "webkom": {
        "username": "Webkom",
        "icon_url": get_URL("webkom"),
    },
    "koskom": {
        "username": "Koskom",
        "icon_url": get_URL("koskom"),
    },
    "labamba": {
        "username": "LaBamba",
        "icon_url": get_URL("labamba"),
    },
    "pr": {
        "username": "PR",
        "icon_url": get_URL("pr"),
    },
    "readme": {
        "username": "readme",
        "icon_url": get_URL("readme"),
    },
    "revy": {
        "username": "Revyen",
        "icon_url": get_URL("revy"),
    },
    "ntnu": {
        "username": "Informasjon fra NTNU",
        "icon_url": get_URL("ntnu"),
    },
}


config = {
    "signing_secret": os.environ.get("SIGNING_SECRET"),
    "oauth_token": os.environ.get("OAUTH_TOKEN"),
    "actions": {
        "x_publish": {
            "channel_id": os.environ.get("CHANNEL_ID"),
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
            "publish_message": lambda config, body: {
                **config["options"]["default"],
                **config["options"][body["submission"]["post_as"]],
                "text": body["submission"]["message"],
                "channel": body["submission"]["channel"],
            },
        },
        "anon_abaquery": {
            "channel_id": os.environ.get("CHANNEL_ID_ABAQUERY"),
            "dialogs": {
                "post_message": lambda body: {
                    "trigger_id": body["trigger_id"],
                    "dialog": {
                        "callback_id": body["callback_id"],
                        "title": "Anonymt spørsmål",
                        "submit_label": "Publiser",
                        "elements": [
                            {
                                "type": "textarea",
                                "label": "Melding",
                                "name": "message",
                            },
                        ],
                    },
                }
            },
            "publish_message": lambda config, body: {
                "username": "Anonym bruker",
                "icon_url": get_URL("abakule"),
                "link_names": True,
                "unfurl_links": True,
                "text": body["submission"]["message"],
                "channel": config["channel_id"],
            },
        },
    },
}


def legal_config():
    return config["signing_secret"] is not None and config["oauth_token"] is not None
