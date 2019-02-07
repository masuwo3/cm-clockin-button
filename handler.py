from myrecorder import clock_in
from slack import post_kaiten


def handler(event, context):
    clock_in()
    post_kaiten()

    return 'ok'
