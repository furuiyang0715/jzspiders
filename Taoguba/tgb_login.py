import pprint
import time
import traceback

import requests
from selenium import webdriver


login_api = 'https://sso.taoguba.com.cn/web/login/submitAli'
login_index = 'https://sso.taoguba.com.cn/web/login/index'


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
}

datas = {
    'userName': 'ruiyang',
    'password': 'qazwsxedc',
    'save': 'Y',
    'checkCode': '''xxxxxx''',
}


def post_api():
    resp = requests.post(login_api, data=datas, headers=headers)
    print(resp)
    if resp and resp.status_code == 200:
        print(resp.text)


def get_cookies():
    loginname = 'ruiyang'
    password = 'qazwsxedc'
    try:
        driver = webdriver.Remote(
            command_executor='http://127.0.0.1:32772/wd/hub',
            desired_capabilities={'browserName': 'chrome'},
        )
        driver.set_window_size(1124, 850)  # 防止得到的WebElement的状态is_displayed为False，即不可见
        driver.get(login_index)
        username = driver.find_element_by_xpath('//input[@id="userName"]')
        # print(username)
        # print(username.clear())
        # print(username.send_keys(loginname))
        # driver.find_element_by_xpath('//[@id="userName"]').send_keys(loginname)
        # time.sleep(2)
        # driver.find_element_by_xpath('//[@id="userPassword"]').send_keys(password)
        # driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()

        cookies = driver.get_cookies()
        print(pprint.pformat(cookies))

        driver.quit()
    except Exception:
        traceback.print_exc()
    finally:
        pass


def sele_login():
    browser = webdriver.Remote(
        command_executor='http://127.0.0.1:32768/wd/hub',
        desired_capabilities={'browserName': 'chrome'},
    )
    browser.get(login_index)
    text = browser.page_source
    # print(text)
    print("loginContent" in text)
    browser.quit()


def main():
    # post_api()

    # sele_login()

    get_cookies()


if __name__ == '__main__':
    main()
