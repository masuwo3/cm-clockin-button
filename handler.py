from myrecorder import record
from slack import post_msg
from slack import change_status


def handler(event, context):
    if "deviceEvent" in event:
        click_type = event["deviceEvent"]["buttonClicked"]["clickType"]

        if click_type == "SINGLE":
            record_type = "CLOCK_IN"
        elif click_type == "DOUBLE":
            record_type = "CLOCK_OUT"
        else:
            # LONGは未実装
            raise Exception(f"Undefined click_type: {click_type}.")
    else:
        raise Exception("This handler can be called from IoT Buttion only.")

    record(record_type)
    post_msg(record_type)
    change_status(record_type)

    return "ok"
