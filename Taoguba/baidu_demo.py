from selenium import webdriver
from time import sleep


driver = webdriver.Remote(
    command_executor='http://127.0.0.1:32768/wd/hub',
    desired_capabilities={'browserName': 'chrome'},
)


driver.get('https://www.baidu.com')
print("get baidu")

driver.find_element_by_id("kw").send_keys("docker selenium")
driver.find_element_by_id("su").click()

sleep(1)

driver.get_screenshot_as_file("/home/fnngj/mypro/baidu_img.png")

driver.quit()
print("end...")
