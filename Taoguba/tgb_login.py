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
    driver = None
    try:
        driver = webdriver.Remote(
            command_executor='http://127.0.0.1:32773/wd/hub',
            desired_capabilities={'browserName': 'chrome'},
        )
        driver.set_window_size(1124, 850)  # 防止得到的 WebElement 的状态 is_displayed 为 False，即不可见
        driver.get(login_index)
        user_name = driver.find_element_by_id('userName')
        user_name.send_keys(loginname)
        pass_word = driver.find_element_by_id('password1')
        pass_word.send_keys(password)
        submit = driver.find_element_by_id('loginbtn1')
        submit.click()
        time.sleep(10)
        driver.refresh()
        cookies = {}
        for cookie in driver.get_cookies():
            cookies[cookie['name']] = cookie['value']
        print(pprint.pformat(cookies))
        return cookies
    except Exception:
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()


def sele_login():
    browser = webdriver.Remote(
        command_executor='http://127.0.0.1:32768/wd/hub',
        desired_capabilities={'browserName': 'chrome'},
    )
    browser.get(login_index)
    text = browser.page_source
    print("loginContent" in text)
    browser.quit()


def main():
    # post_api()

    # sele_login()
    # cookies = {}

    # cookies = get_cookies()
    # cookies = 'UM_distinctid=174a0a9ce9e9bc-0938a67e9ceea3-31667305-1fa400-174a0a9ce9fb16; CNZZDATA1574657=cnzz_eid%3D1766937287-1600418930-%26ntime%3D1600418930; Hm_lvt_cc6a63a887a7d811c92b7cc41c441837=1600423317; tgbuser=3707036; tgbpwd=788435B9672s589xtktbhcmeck; JSESSIONID=c60096ce-aabd-401f-b4c1-059ce998e465; Hm_lpvt_cc6a63a887a7d811c92b7cc41c441837=1600423321'
    cookies = 'tgbuser=3707036; tgbpwd=788435B9672s589xtktbhcmeck; UM_distinctid=174a09f38717dc-0dbb36cdfd7688-31667305-1fa400-174a09f3872ca7; CNZZDATA1574657=cnzz_eid%3D1288858779-1600418930-https%253A%252F%252Fsso.taoguba.com.cn%252F%26ntime%3D1600418930; Hm_lvt_cc6a63a887a7d811c92b7cc41c441837=1600422623; JSESSIONID=a8f41248-de23-46f6-9a20-f33cb7ef431a; Hm_lpvt_cc6a63a887a7d811c92b7cc41c441837=1600422820'

    url = 'https://www.taoguba.com.cn/quotes/getStockUpToDate?stockCode=sz000651&actionDate=1600422266000&perPageNum=20&isOpen=false'
    headers.update({"cookie": cookies})
    resp = requests.get(url, headers=headers)
    print(resp)
    print(resp.text)


if __name__ == '__main__':
    main()


'''
https://my.oschina.net/fxtxz2/blog/3055390

http://www.python3.vip/tut/auto/selenium/01/ 


sudo docker run -d -P --name myhub selenium/hub 
sudo docker run -d --link myhub:hub --name node selenium/node-chrome 


tgbuser=3707036; 
tgbpwd=788435B9672s589xtktbhcmeck; 

UM_distinctid=174a09f38717dc-0dbb36cdfd7688-31667305-1fa400-174a09f3872ca7; 
CNZZDATA1574657=cnzz_eid%3D1288858779-1600418930-https%253A%252F%252Fsso.taoguba.com.cn%252F%26ntime%3D1600418930; 
Hm_lvt_cc6a63a887a7d811c92b7cc41c441837=1600422623; 
JSESSIONID=a8f41248-de23-46f6-9a20-f33cb7ef431a; 
Hm_lpvt_cc6a63a887a7d811c92b7cc41c441837=1600422820 


'''