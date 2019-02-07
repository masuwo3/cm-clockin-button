from time import sleep
from datetime import datetime
import json

import boto3
from selenium import webdriver

CHROME_DRIVER_PATH = "/opt/python/bin/chromedriver"
SECRET_NAME = "cm-clockin-button/myrecorder"


def clock_in():
    driver = __webdriver()
    driver.get("https://s2.kingtime.jp/independent/recorder/personal/")

    login_id, passwd = __secrets()

    try:
        # ログイン
        id_form = driver.find_element_by_id('id')
        id_form.send_keys(login_id)

        password_form = driver.find_element_by_id('password')
        password_form.send_keys(passwd)

        login_btn = driver.find_element_by_xpath(
                                '//*[@id="modal_window"]/div/div/div[3]/div')
        login_btn.click()

        sleep(5)

        # 打刻
        clockin_btn = driver.find_element_by_xpath(
                    '//*[@id="record_qmXXCxw9WEWN3X/YrkMWuQ=="]/div/div[2]')
        clockin_btn.click()
        driver.close()
    except Exception as e:
        # ブラウザ操作が失敗した場合はSSをアップロードする。
        today = datetime.today().strftime('%Y%m%d%H%M%S')
        driver.save_screenshot(f'/tmp/{today}.png')
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(f'/tmp/{today}.png',
                                   'cm-hiratakei-hogehoge',
                                   f'{today}.png')
        print('upload screenshot: s3://cm-hiratakei-hogehoge/{today}.png')
        raise e


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
    sm = boto3.client('secretsmanager')
    secrets = json.loads(
                    sm.get_secret_value(SecretId=SECRET_NAME)['SecretString'])

    login_id = secrets['id']
    passwd = secrets['passwd']

    return (login_id, passwd)
