from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.config import Config


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)

    def find_element(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def click_element(self, by, value):
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
        return element

    def send_keys_to_element(self, by, value, text):
        element = self.find_element(by, value)
        element.click()
        time.sleep(0.5)
        element.send_keys(text)
        return element

    def get_element_attribute(self, by, value, attribute_name):
        element = self.find_element(by, value)
        return element.get_attribute(attribute_name)

    def is_element_displayed(self, by, value):
        try:
            element = self.find_element(by, value)
            return element.is_displayed()
        except:
            return False

    def get_page_source(self):
        return self.driver.page_source

    def take_screenshot(self, filename):
        filepath = os.path.join(Config.SCREENSHOT_DIR, filename)
        self.driver.save_screenshot(filepath)
        return filepath

    def wait_seconds(self, seconds):
        time.sleep(seconds)

    def take_screenshot_on_failure(self, test_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"error_{test_name}_{timestamp}.png"
        filepath = os.path.join(Config.SCREENSHOT_DIR, filename)

        try:
            self.driver.save_screenshot(filepath)
            print(f"\nHATA SS: {filepath}\n")
            return filepath
        except Exception as e:
            print(f"\nScreenshot alinamadi: {e}\n")
            return None