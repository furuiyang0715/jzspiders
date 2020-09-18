from selenium import webdriver

browser = webdriver.Chrome()

# browser = webdriver.Remote(
#     command_executor='http://127.0.0.1:32768/wd/hub',
#     desired_capabilities={'browserName': 'chrome'},
# )
browser.get('http://www.baidu.com/')
text = browser.page_source
print(text)
browser.quit()
