import json

import boto3
import requests

URL = "https://slack.com/api/chat.postMessage"
CHANNEL = "#team-aws-bu-kaiten"
SECRET_NAME = "cm-clockin-button/slack"


def post_kaiten():
    payload = {
        "token": __secret_token(),
        "text": "開店",
        "channel": CHANNEL,
        "as_user": True
    }

    # 開店宣言
    resp = requests.post(URL, data=payload)
    resp.raise_for_status()


def __secret_token():
    sm = boto3.client('secretsmanager')
    secrets = json.loads(
                    sm.get_secret_value(SecretId=SECRET_NAME)['SecretString'])

    return secrets['token']
