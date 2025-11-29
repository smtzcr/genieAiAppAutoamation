from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
import time
from .base_page import BasePage
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.config import Config


class ChatPage(BasePage):

    MODEL_BOX = (AppiumBy.ACCESSIBILITY_ID, "ai_model_box")
    MODEL_SEARCH_INPUT = (AppiumBy.ACCESSIBILITY_ID, "main_model_selector_search_input")
    MESSAGE_INPUT = (AppiumBy.ACCESSIBILITY_ID, "main_chat_input")
    SEND_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "main_chat_send_button")
    AI_MESSAGE_BOX = (AppiumBy.ACCESSIBILITY_ID, "ai_message_box")

    def get_current_model(self):
        model_box = self.find_element(*self.MODEL_BOX)
        return model_box.get_attribute("label") or model_box.get_attribute("name")

    def open_model_dropdown(self):
        print("Model dropdown aciliyor...")
        current_model = self.get_current_model()
        print(f"Su anki model: {current_model}")
        self.click_element(*self.MODEL_BOX)
        print("Model dropdown acildi")
        time.sleep(2)
        return current_model

    def search_model(self, model_name):
        print(f"'{model_name}' aranıyor...")
        search_input = self.find_element(*self.MODEL_SEARCH_INPUT)
        search_input.click()
        time.sleep(1)
        print(f"'{model_name}' yaziliyor...")
        search_input.send_keys(model_name)
        time.sleep(2)
        print("Arama tamamlandi")

    def select_model_from_results(self, model_name):
        print(f"'{model_name}' seciliyor...")

        possible_selectors = [
            (AppiumBy.XPATH, f"//*[contains(@label, '{model_name}')]"),
            (AppiumBy.XPATH, f"//*[contains(@name, '{model_name}')]"),
            (AppiumBy.XPATH, f"//XCUIElementTypeStaticText[contains(@label, '{model_name}')]"),
            (AppiumBy.XPATH, f"//XCUIElementTypeButton[contains(@label, '{model_name}')]"),
            (AppiumBy.XPATH, f"//XCUIElementTypeCell[contains(@label, '{model_name}')]"),
        ]

        for selector_type, selector_value in possible_selectors:
            try:
                element = self.wait.until(
                    EC.presence_of_element_located((selector_type, selector_value))
                )
                if element:
                    element.click()
                    print(f"'{model_name}' secildi!")
                    time.sleep(2)
                    return True
            except:
                continue

        print(f"'{model_name}' elementi bulunamadi")
        self.take_screenshot('model_selection_failed.png')
        return False

    def select_model(self, model_name=None):
        if model_name is None:
            model_name = Config.DEFAULT_MODEL

        self.open_model_dropdown()
        self.search_model(model_name)
        success = self.select_model_from_results(model_name)

        if success:
            selected_model = self.get_current_model()
            print(f"Yeni secilen model: {selected_model}")

        return success

    def get_message_input_value(self):
        message_input = self.find_element(*self.MESSAGE_INPUT)
        return message_input.get_attribute("value") or message_input.text or ""

    def type_message(self, message):
        print(f"Mesaj yaziliyor: '{message}'")
        self.send_keys_to_element(*self.MESSAGE_INPUT, message)
        print("Mesaj yazildi")
        time.sleep(1)

    def click_send_button(self):
        print("Mesaj gonderiliyor...")
        self.click_element(*self.SEND_BUTTON)
        print("Gonder butonuna basildi")
        time.sleep(3)

    def is_message_sent(self):
        time.sleep(1)
        message_input = self.find_element(*self.MESSAGE_INPUT)
        current_value = message_input.get_attribute("value") or ""
        placeholder = message_input.get_attribute("placeholderValue") or ""

        is_empty = current_value.strip() == "" or current_value.strip() == placeholder.strip()

        if is_empty:
            print("Input alani temizlendi (mesaj gonderildi)")
        else:
            print(f"Input alani temizlenmedi: '{current_value}'")

        return is_empty

    def wait_for_response(self, wait_time=None):
        if wait_time is None:
            wait_time = Config.AI_RESPONSE_WAIT_TIME

        print(f"AI'dan cevap bekleniyor ({wait_time} saniye)...")
        time.sleep(wait_time)

    def is_ai_response_received(self):
        try:
            ai_message = self.find_element(*self.AI_MESSAGE_BOX)
            if ai_message:
                print("AI cevap kutusu bulundu")
                return True
        except:
            print("AI cevap kutusu bulunamadi")
            return False

    def send_message(self, message):
        self.type_message(message)
        self.click_send_button()
        return self.is_message_sent()