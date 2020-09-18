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

    sele_login()


if __name__ == '__main__':
    main()
