from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
import time
from .base_page import BasePage
import sys
import os

# Config modülünü import edebilmek için path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.config import Config


class ChatPage(BasePage):
    """
    GenieChat ana sayfası - Model seçimi ve mesajlaşma
    """

    # ========== LOCATORS ==========

    # Model Selection Locators
    MODEL_BOX = (AppiumBy.ACCESSIBILITY_ID, "ai_model_box")
    MODEL_SEARCH_INPUT = (AppiumBy.ACCESSIBILITY_ID, "main_model_selector_search_input")

    # Chat Locators
    MESSAGE_INPUT = (AppiumBy.ACCESSIBILITY_ID, "main_chat_input")
    SEND_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "main_chat_send_button")

    # ========== MODEL SELECTION METHODS ==========

    def get_current_model(self):
        """
        Şu anki seçili modeli döndür

        Returns:
            str: Model adı
        """
        model_box = self.find_element(*self.MODEL_BOX)
        return model_box.get_attribute("label") or model_box.get_attribute("name")

    def open_model_dropdown(self):
        """
        Model dropdown'ını aç

        Returns:
            str: Dropdown açılmadan önceki model adı
        """
        print("🤖 Model dropdown açılıyor...")
        current_model = self.get_current_model()
        print(f"📊 Şu anki model: {current_model}")

        self.click_element(*self.MODEL_BOX)
        print("✅ Model dropdown açıldı")
        time.sleep(2)

        return current_model

    def search_model(self, model_name):
        """
        Model adına göre arama yap

        Args:
            model_name: Aranacak model adı
        """
        print(f"🔍 '{model_name}' aranıyor...")

        # Search input'u bul ve tıkla
        search_input = self.find_element(*self.MODEL_SEARCH_INPUT)
        search_input.click()
        time.sleep(1)

        # Model adını yaz
        print(f"⌨️  '{model_name}' yazılıyor...")
        search_input.send_keys(model_name)
        time.sleep(2)
        print("✅ Arama tamamlandı")

    def select_model_from_results(self, model_name):
        """
        Arama sonuçlarından modeli seç

        Args:
            model_name: Seçilecek model adı

        Returns:
            bool: Başarılı ise True
        """
        print(f"🎯 '{model_name}' seçiliyor...")

        # Olası selector'lar
        possible_selectors = [
            (AppiumBy.XPATH, f"//*[contains(@label, '{model_name}')]"),
            (AppiumBy.XPATH, f"//*[contains(@name, '{model_name}')]"),
            (AppiumBy.XPATH, f"//XCUIElementTypeStaticText[contains(@label, '{model_name}')]"),
            (AppiumBy.XPATH, f"//XCUIElementTypeButton[contains(@label, '{model_name}')]"),
            (AppiumBy.XPATH, f"//XCUIElementTypeCell[contains(@label, '{model_name}')]"),
        ]

        # Her selector'ı dene
        for selector_type, selector_value in possible_selectors:
            try:
                element = self.wait.until(
                    EC.presence_of_element_located((selector_type, selector_value))
                )
                if element:
                    element.click()
                    print(f"✅ '{model_name}' seçildi!")
                    time.sleep(2)
                    return True
            except:
                continue

        # Debug: Bulunamazsa
        print(f"⚠️  '{model_name}' elementi bulunamadı, debug yapılıyor...")
        self.take_screenshot('model_selection_failed.png')

        with open('model_selection_debug.xml', 'w', encoding='utf-8') as f:
            f.write(self.get_page_source())

        print("💾 Debug dosyaları: model_selection_failed.png, model_selection_debug.xml")
        return False

    def select_model(self, model_name=None):
        """
        Model seç (ana metod)

        Args:
            model_name: Seçilecek model adı (varsayılan: Config'den alınır)

        Returns:
            bool: Başarılı ise True
        """
        if model_name is None:
            model_name = Config.DEFAULT_MODEL

        self.open_model_dropdown()
        self.search_model(model_name)
        success = self.select_model_from_results(model_name)

        if success:
            selected_model = self.get_current_model()
            print(f"📊 Yeni seçilen model: {selected_model}")
            self.take_screenshot('model_selected.png')

        return success

    # ========== CHAT METHODS ==========

    def get_message_input_value(self):
        """
        Mesaj input alanındaki değeri al

        Returns:
            str: Input alanındaki metin
        """
        message_input = self.find_element(*self.MESSAGE_INPUT)
        return message_input.get_attribute("value") or message_input.text or ""

    def type_message(self, message):
        """
        Mesaj input alanına yaz

        Args:
            message: Yazılacak mesaj
        """
        print(f"📝 Mesaj yazılıyor: '{message}'")
        self.send_keys_to_element(*self.MESSAGE_INPUT, message)
        print("✅ Mesaj yazıldı")
        time.sleep(1)

    def click_send_button(self):
        """
        Gönder butonuna tıkla
        """
        print("📤 Mesaj gönderiliyor...")
        self.click_element(*self.SEND_BUTTON)
        print("✅ Gönder butonuna basıldı")
        time.sleep(2)

    def is_message_sent(self):
        """
        Mesajın gönderildiğini kontrol et (input temizlendi mi?)

        Returns:
            bool: Mesaj gönderildiyse True
        """
        current_value = self.get_message_input_value()
        is_empty = current_value.strip() == ""

        if is_empty:
            print("✅ Input alanı temizlendi (mesaj gönderildi)")
        else:
            print(f"⚠️  Input alanı temizlenmedi: '{current_value}'")

        return is_empty

    def wait_for_response(self, wait_time=None):
        """
        AI cevabını bekle

        Args:
            wait_time: Bekleme süresi (saniye). None ise Config'den alınır
        """
        if wait_time is None:
            wait_time = Config.AI_RESPONSE_WAIT_TIME

        print(f"⏳ AI'dan cevap bekleniyor ({wait_time} saniye)...")
        time.sleep(wait_time)

    def send_message(self, message):
        """
        Mesaj gönderme - tam akış

        Args:
            message: Gönderilecek mesaj

        Returns:
            bool: Mesaj başarıyla gönderildiyse True
        """
        self.type_message(message)
        self.click_send_button()
        return self.is_message_sent()