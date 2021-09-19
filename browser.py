from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import requests, time
from selenium.common.exceptions import NoSuchElementException


class Browser(object):
    _instance_list = {}

    def __init__(self, host, port, profile_id, chrome_driver):

        status, result = self._get_vm_browser_config(host, port, profile_id)
        if not status:
            raise ValueError(result)

        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", result)
        self._driver = webdriver.Chrome(chrome_driver, options=chrome_options)

    def get(self, url):
        self._driver.get(url)

    def click(self, xpath, time_sleep=1):
        self._driver.find_element_by_xpath(xpath).click()
        if time_sleep:
            time.sleep(time_sleep)

    def send_keys(self, xpath, value, time_sleep=1):
        element = self._driver.find_element_by_xpath(xpath)
        element.send_keys(value)  # send_keys
        if time_sleep:
            time.sleep(time_sleep)

    def close(self):
        self._driver.close()

    def implicitly_wait(self, timeout):
        self._driver.implicitly_wait(timeout)

    def implicitly_wait(self, timeout):
        self._driver.implicitly_wait(timeout)

    def web_driver_wait(self, timeout=10, poll_frequency=1, ignored_exceptions=None):
        return WebDriverWait(self._driver, timeout, poll_frequency, ignored_exceptions)

    def webdriver_wait_until(self, timeout, method, poll_frequency=0.5, ignored_exceptions=None):
        element = WebDriverWait(self._driver, timeout, poll_frequency, ignored_exceptions).until(method)
        return element

    def is_display(self, xpath):
        try:
            element = self._driver.find_element_by_xpath(xpath)
            return element.is_displayed()
        except NoSuchElementException:
            return False

    @staticmethod
    def _get_vm_browser_config(host, port, profile_id):
        """获取浏览器配置"""
        url = f'http://{host}:{port}/api/v1/profile/start?automation=true&profileId={profile_id}'

        try:
            response = requests.get(url).json()
            if not response or response.get("status") == "ERROR":
                msg = response.get("value") if response else "获取配置信息为空"
                return False, msg
            _, browser_port = response.get("value")[7:].split(":")
            return True, f"{host}:{browser_port}"

        except Exception as e:
            return False, "连接浏览器失败"

    def __getattr__(self, name):
        if hasattr(self._driver, name):
            return getattr(self._driver, name)
