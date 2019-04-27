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
            'https://avatars2.githubusercontent.com/u/10448101?s=200&v=4',
            'link_names':
            True,
            "unfurl_links":
            True
        },
        'hovedstyret': {
            'username': 'Hovedstyret',
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
