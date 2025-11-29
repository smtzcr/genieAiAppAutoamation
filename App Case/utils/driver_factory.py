from appium import webdriver
from appium.options.ios import XCUITestOptions
import sys
import os

# Config modülünü import edebilmek için path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.config import Config


class DriverFactory:
    @staticmethod
    def create_driver():
        """
        Appium driver oluştur

        Returns:
            WebDriver: Appium driver instance
        """

        options = XCUITestOptions()
        options.platform_name = Config.PLATFORM_NAME
        options.device_name = Config.DEVICE_NAME
        options.udid = Config.UDID
        options.bundle_id = Config.BUNDLE_ID
        options.automation_name = Config.AUTOMATION_NAME
        options.no_reset = Config.NO_RESET

        driver = webdriver.Remote(Config.APPIUM_SERVER, options=options)

        driver.implicitly_wait(Config.IMPLICIT_WAIT)

        print(f"✅ Driver oluşturuldu: {Config.BUNDLE_ID}")
        print(f"📱 Cihaz: {Config.DEVICE_NAME} (UDID: {Config.UDID})")

        return driver

    @staticmethod
    def quit_driver(driver):
        if driver:
            print("🔌 Driver kapatılıyor...")
            driver.quit()
            print("✅ Driver kapatıldı")