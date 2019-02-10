from time import sleep
from datetime import datetime
import json
import os

import boto3
from selenium import webdriver

CHROME_DRIVER_PATH = "/opt/python/bin/chromedriver"
SECRET_NAME = "cm-clockin-button/myrecorder"

LOGIN_BTN_XPATH = '//*[@id="modal_window"]/div/div/div[3]/div'
CLOCK_IN_BTN_XPATH = '//*[@id="record_qmXXCxw9WEWN3X/YrkMWuQ=="]/div'
CLOCK_OUT_BTN_XPATH = '//*[@id="record_j8ekmJaw6W3M4w3i6hlSIQ=="]/div'


def record(record_type):
    driver = __webdriver()
    driver.get("https://s2.kingtime.jp/independent/recorder/personal/")

    login_id, passwd = __secrets()

    try:
        __login(driver, login_id, passwd)
        sleep(5)

        if record_type == "CLOCK_IN":
            __record(driver, CLOCK_IN_BTN_XPATH)
        elif record_type == "CLOCK_OUT":
            __record(driver, CLOCK_OUT_BTN_XPATH)

        driver.close()
    except Exception as e:
        # ブラウザ操作が失敗した場合はSSをアップロードする。
        today = datetime.today().strftime("%Y%m%d%H%M%S")
        driver.save_screenshot(f"/tmp/{today}.png")
        driver.close()

        bucket_name = os.environ["BACKUP_BUCKET"]
        s3 = boto3.resource("s3")
        s3.meta.client.upload_file(f"/tmp/{today}.png",
                                   bucket_name,
                                   f"{today}.png")
        print(f"upload screenshot: s3://{bucket_name}/{today}.png")
        raise e


def __login(driver, login_id, passwd):
    id_form = driver.find_element_by_id("id")
    id_form.send_keys(login_id)

    password_form = driver.find_element_by_id("password")
    password_form.send_keys(passwd)

    login_btn = driver.find_element_by_xpath(LOGIN_BTN_XPATH)
    login_btn.click()


def __record(driver, btn_xpath):
    btn = driver.find_element_by_xpath(btn_xpath)
    btn.click()


def __webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=0")
    options.add_argument("--v=99")
    options.add_argument("--single-process")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--homedir=/tmp")
    options.binary_location = "/opt/python/bin/headless-chromium"

    return webdriver.Chrome(CHROME_DRIVER_PATH, chrome_options=options)


def __secrets():
    sm = boto3.client("secretsmanager")
    secrets = json.loads(
                    sm.get_secret_value(SecretId=SECRET_NAME)["SecretString"])

    login_id = secrets["id"]
    passwd = secrets["passwd"]

    return (login_id, passwd)
