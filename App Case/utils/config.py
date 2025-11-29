class Config:
    """Test konfigürasyon sınıfı"""

    APPIUM_SERVER = 'http://127.0.0.1:4723'
    PLATFORM_NAME = 'iOS'
    DEVICE_NAME = 'iPhone'
    UDID = '00008110-000965D61402601E'
    AUTOMATION_NAME = 'XCUITest'

    BUNDLE_ID = 'co.appnation.geniechat'
    NO_RESET = True

    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 15

    DEFAULT_MODEL = 'GPT-5 Nano'
    DEFAULT_MESSAGE = 'Merhaba, nasılsın?'
    AI_RESPONSE_WAIT_TIME = 15

    SCREENSHOT_DIR = '.'

    @classmethod
    def get_capabilities(cls):
        return {
            'platformName': cls.PLATFORM_NAME,
            'appium:deviceName': cls.DEVICE_NAME,
            'appium:udid': cls.UDID,
            'appium:bundleId': cls.BUNDLE_ID,
            'appium:automationName': cls.AUTOMATION_NAME,
            'appium:noReset': cls.NO_RESET,
        }