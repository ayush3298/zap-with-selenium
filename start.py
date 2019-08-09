from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time


class starter:
    def __init__(self):
        PROXY = "127.0.0.1:8080"
        # b7045872@urhen.com
        # Upload@task
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY,
            "noProxy": None,
            "proxyType": "MANUAL",
            "class": "org.openqa.selenium.Proxy",
            "autodetect": False
        }

        self.driver = webdriver.Chrome('/home/ayush/Downloads/chromedriver',
                                       desired_capabilities=webdriver.DesiredCapabilities.CHROME)

    def login(self, email, password):
        self.driver.get('https://secure.indeed.com/account/login')
        self.driver.find_element_by_xpath('//*[@id="login-email-input"]').send_keys(email)
        self.driver.find_element_by_xpath('//*[@id="login-password-input"]').send_keys(password)

        try:
            self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/button').click()
            self.driver.find_element_by_xpath('//*[@id="login-submit-button"]').click()

        except NoSuchElementException:
            self.driver.find_element_by_xpath('//*[@id="login-submit-button"]').click()
        time.sleep(100)


s = starter()
s.login('b7045872@urhen.com', 'Upload@task')
