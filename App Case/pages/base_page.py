"""
Base Page - Tüm page object'lerin parent sınıfı
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import sys
import os

# Config modülünü import edebilmek için path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.config import Config


class BasePage:
    """
    Tüm page object'ler için temel sınıf.
    Ortak metodları içerir.
    """

    def __init__(self, driver):
        """
        BasePage constructor

        Args:
            driver: Appium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)

    def find_element(self, by, value):
        """
        Element bulma - bekleme ile

        Args:
            by: Locator stratejisi (AppiumBy.ID, AppiumBy.XPATH, vb.)
            value: Locator değeri

        Returns:
            WebElement: Bulunan element
        """
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def click_element(self, by, value):
        """
        Element bulma ve tıklama

        Args:
            by: Locator stratejisi
            value: Locator değeri

        Returns:
            WebElement: Tıklanan element
        """
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
        return element

    def send_keys_to_element(self, by, value, text):
        """
        Element bulma ve metin gönderme

        Args:
            by: Locator stratejisi
            value: Locator değeri
            text: Gönderilecek metin

        Returns:
            WebElement: Element
        """
        element = self.find_element(by, value)
        element.click()
        time.sleep(0.5)
        element.send_keys(text)
        return element

    def get_element_attribute(self, by, value, attribute_name):
        """
        Element attribute değerini al

        Args:
            by: Locator stratejisi
            value: Locator değeri
            attribute_name: Attribute adı (label, name, value, vb.)

        Returns:
            str: Attribute değeri
        """
        element = self.find_element(by, value)
        return element.get_attribute(attribute_name)

    def is_element_displayed(self, by, value):
        """
        Elementin görünür olup olmadığını kontrol et

        Args:
            by: Locator stratejisi
            value: Locator değeri

        Returns:
            bool: Element görünürse True
        """
        try:
            element = self.find_element(by, value)
            return element.is_displayed()
        except:
            return False

    def get_page_source(self):
        """
        Sayfa kaynağını al

        Returns:
            str: Sayfa XML kaynağı
        """
        return self.driver.page_source

    def take_screenshot(self, filename):
        """
        Ekran görüntüsü al

        Args:
            filename: Dosya adı (örn: 'screenshot.png')

        Returns:
            str: Dosya adı
        """
        filepath = os.path.join(Config.SCREENSHOT_DIR, filename)
        self.driver.save_screenshot(filepath)
        return filepath

    def wait_seconds(self, seconds):
        """
        Belirtilen süre bekle

        Args:
            seconds: Bekleme süresi (saniye)
        """
        time.sleep(seconds)

    def take_screenshot_on_failure(self, test_name):
        """
        Hata durumunda otomatik ekran görüntüsü al
        Dosya adı: error_<test_name>_<timestamp>.png
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"error_{test_name}_{timestamp}.png"
        filepath = os.path.join(Config.SCREENSHOT_DIR, filename)

        try:
            self.driver.save_screenshot(filepath)
            print(f"\n❌ HATA SS: {filepath}\n")
            return filepath
        except Exception as e:
            print(f"\n⚠️  Screenshot alınamadı: {e}\n")
            return None