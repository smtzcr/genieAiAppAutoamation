import unittest
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.chat_page import ChatPage
from utils.driver_factory import DriverFactory
from utils.config import Config


class TestGenieChatMainFlow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nTest sinifi baslatiliyor...")
        cls.driver = DriverFactory.create_driver()
        print("Appium baglantisi kuruldu\n")
        time.sleep(3)
        cls.chat_page = ChatPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        print("\nTest sinifi sonlandiriliyor...")
        DriverFactory.quit_driver(cls.driver)
        print("Baglanti kapatildi\n")

    def setUp(self):
        print(f"\nTest basliyor: {self._testMethodName}")
        self._test_failed = False

    def tearDown(self):
        if self._test_failed or (hasattr(self._outcome, 'errors') and any(self._outcome.errors)):
            try:
                self.chat_page.take_screenshot_on_failure(self._testMethodName)
            except Exception as e:
                print(f"Screenshot alinamadi: {e}")
        print(f"Test tamamlandi: {self._testMethodName}\n")

    def run(self, result=None):
        self._outcome = result
        return super().run(result)

    def test_send_message_with_free_model_and_verify_response(self):
        try:
            print("\nModel secimi basladi")
            model_selected = self.chat_page.select_model(Config.DEFAULT_MODEL)
            self.assertTrue(model_selected, f"{Config.DEFAULT_MODEL} modeli secilemedi!")

            current_model = self.chat_page.get_current_model()
            self.assertIsNotNone(current_model, "Model bilgisi alinamadi!")
            print(f"Model secildi: {current_model}\n")

            print("Mesaj gonderme basladi")
            test_message = Config.DEFAULT_MESSAGE

            self.chat_page.type_message(test_message)

            input_value = self.chat_page.get_message_input_value()
            self.assertIn("Merhaba", str(input_value),
                          "Mesaj input alanina yazilmadi!")

            self.chat_page.click_send_button()

            message_sent = self.chat_page.is_message_sent()
            self.assertTrue(message_sent,
                            "Mesaj gonderildikten sonra input alani temizlenmedi!")

            print("\nCevap bekleniyor")
            self.chat_page.wait_for_response()

            ai_response_received = self.chat_page.is_ai_response_received()
            self.assertTrue(ai_response_received, "AI'dan cevap gelmedi - AI mesaj kutusu bulunamadi!")

            screenshot_path = self.chat_page.take_screenshot('genie_final_test.png')
            print(f"Ekran goruntusu kaydedildi: {screenshot_path}")

            print(f"\nTest basarili")
            print(f"Model: {Config.DEFAULT_MODEL}")
            print(f"Mesaj: '{test_message}'")
            print("AI cevap kutusu basariyla bulundu")

        except AssertionError as e:
            self._test_failed = True
            print(f"\nAssertion hatasi: {e}")
            self.chat_page.take_screenshot_on_failure(self._testMethodName)
            raise

        except Exception as e:
            self._test_failed = True
            print(f"\nBeklenmeyen hata: {e}")
            self.chat_page.take_screenshot_on_failure(self._testMethodName)
            raise


if __name__ == '__main__':
    unittest.main(verbosity=2)