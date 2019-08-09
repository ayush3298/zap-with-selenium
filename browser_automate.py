from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class automated_browser:
    def __init__(self, proxy_url):
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": proxy_url,
            "ftpProxy": proxy_url,
            "sslProxy": proxy_url,
            "noProxy": None,
            "proxyType": "MANUAL",
            "class": "org.openqa.selenium.Proxy",
            "autodetect": False
        }

        self.driver = webdriver.Chrome('/home/ayush/Downloads/chromedriver',
                                       desired_capabilities=webdriver.DesiredCapabilities.CHROME)
        self.login('b7045872@urhen.com', 'Upload@task')
        self.driver.quit()

    def login(self, email, password):
            self.driver.get('https://secure.indeed.com/account/login')
            self.driver.find_element_by_xpath('//*[@id="login-email-input"]').send_keys(email)
            self.driver.find_element_by_xpath('//*[@id="login-password-input"]').send_keys(password)

            try:
                self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/button').click()
                self.driver.find_element_by_xpath('//*[@id="login-submit-button"]').click()

            except NoSuchElementException:
                self.driver.find_element_by_xpath('//*[@id="login-submit-button"]').click()
