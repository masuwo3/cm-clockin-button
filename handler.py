from selenium import webdriver


def clockin_handler(event, context):
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
    options.binary_location = "./bin/headless-chromium"

    driver = webdriver.Chrome(
        "/opt/python/bin/chromedriver", chrome_options=options)
    driver.get("https://s2.kingtime.jp/independent/recorder/personal/")

    # ログイン
    id_form = driver.find_element_by_id('id')
    id_form.send_keys('cls30243')
    password_form = driver.find_element_by_id('password')
    password_form.send_keys('PrWmHKmzGK8y7rDrLhZF')
    login_btn = driver.find_element_by_xpath(
                            '//*[@id="modal_window"]/div/div/div[3]/div')
    login_btn.click()

    # 打刻処理
    clockin_btn = driver.find_element_by_xpath(
                    '//*[@id="record_qmXXCxw9WEWN3X/YrkMWuQ=="]/div/div[2]')
    clockin_btn.click()

    driver.close()
    return 'hoge'
