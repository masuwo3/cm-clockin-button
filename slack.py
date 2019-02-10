from datetime import date
from datetime import time
from datetime import datetime
from datetime import timezone
import json

import boto3
import requests

POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"
SET_PROFILE_URL = "https://slack.com/api/users.profile.set"
CHANNEL = "#team-aws-bu-kaiten"
SECRET_NAME = "cm-clockin-button/slack"

WORKING_PROFILE = {"status_text": "働いています",
                   "status_emoji": ":hatarakihoudai:"}

RESET_PROFILE = {"status_text": "",
                 "status_emoji": ""}


def post_msg(record_type):
    if record_type == "CLOCK_IN":
        text = "開店"
    elif record_type == "CLOCK_OUT":
        text = "閉店"
    else:
        return

    payload = {
        "token": __secret_token(),
        "text": text,
        "channel": CHANNEL,
        "as_user": True}

    # 開店/閉店宣言
    resp = requests.post(POST_MESSAGE_URL, data=payload)
    resp.raise_for_status()


def change_status(record_type):
    if record_type == "CLOCK_IN":
        profile = WORKING_PROFILE
        profile["status_expiration"] = __end_of_day()
    elif record_type == "CLOCK_OUT":
        profile = RESET_PROFILE

    payload = {
        "token": __secret_token(),
        "profile": json.dumps(profile)}

    # ステータス変更
    resp = requests.post(SET_PROFILE_URL, data=payload)
    resp.raise_for_status()


def __secret_token():
    sm = boto3.client("secretsmanager")
    secrets = json.loads(
                    sm.get_secret_value(SecretId=SECRET_NAME)["SecretString"])

    return secrets["token"]


def __end_of_day():
    eod = datetime.combine(date.today(),
                           time.max,
                           tzinfo=timezone.utc)

    return round(eod.timestamp())
