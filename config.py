import os

config = {
    'signing_secret': os.environ.get('SIGNING_SECRET'),
    'target_webhook': os.environ.get('TARGET_WEBHOOK'),
    'oauth_token': os.environ.get('OAUTH_TOKEN'),
    'options': {
        'default': {
            'username':
            'Abakus',
            'icon_url':
            'https://github.com/JonasBak/abakus-fwd/blob/master/icons/abakule.png?raw=true',
            'link_names':
            True,
            "unfurl_links":
            True
        },
        'hovedstyret': {
            'username': 'Hovedstyret',
            'icon_url':
            'https://github.com/JonasBak/abakus-fwd/blob/master/icons/hs.png?raw=true',
        },
        'bedriftskontakt': {
            'username': 'Bedriftskontakt',
            'icon_url':
            'https://github.com/JonasBak/abakus-fwd/blob/master/icons/bedkom.png?raw=true',
        }
    },
    'dialogs': {
        'post_message': lambda body: {
            'trigger_id': body['trigger_id'],
            'dialog': {
                'callback_id':
                'x_publish',
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
                                     {
                                         'label': 'Bedriftskontakt',
                                         'value': 'bedriftskontakt'
                                     },
                                     {
                                         'label': 'Abakus',
                                         'value': 'default'
                                     },
                                 ]
                             }]
            }
        }
    }
}


def legal_config():
    return config['signing_secret'] is not None and config[
        'target_webhook'] is not None and config['oauth_token'] is not None
