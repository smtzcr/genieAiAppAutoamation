"""
GenieChat iOS Test - unittest test sınıfı
"""
import unittest
import sys
import os
import time

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.chat_page import ChatPage
from utils.driver_factory import DriverFactory
from utils.config import Config


class TestGenieChatMainFlow(unittest.TestCase):
    """
    GenieChat iOS uygulama testleri
    """

    @classmethod
    def setUpClass(cls):
        """
        Test sınıfı başlamadan önce bir kez çalışır
        Appium bağlantısı kurar
        """
        print("\n" + "=" * 60)
        print("🚀 Test sınıfı başlatılıyor...")
        print("=" * 60)

        # Driver oluştur
        cls.driver = DriverFactory.create_driver()

        print("✅ Appium bağlantısı kuruldu\n")
        time.sleep(3)

        # Page Object başlat
        cls.chat_page = ChatPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        """
        Tüm testler bittikten sonra çalışır
        Driver'ı kapatır
        """
        print("\n" + "=" * 60)
        print("🏁 Test sınıfı sonlandırılıyor...")
        print("=" * 60)

        # Driver'ı kapat
        DriverFactory.quit_driver(cls.driver)

        print("✅ Bağlantı kapatıldı\n")

    def setUp(self):
        """
        Her test öncesi çalışır
        """
        print(f"\n▶️  Test başlıyor: {self._testMethodName}")
        print("-" * 60)
        # Test sonucunu takip etmek için flag
        self._test_failed = False

    def tearDown(self):
        """
        Her test sonrası çalışır
        Hata varsa screenshot alır
        """
        # Test başarısız olduysa screenshot al
        if self._test_failed or (hasattr(self._outcome, 'errors') and any(self._outcome.errors)):
            try:
                self.chat_page.take_screenshot_on_failure(self._testMethodName)
            except Exception as e:
                print(f"⚠️  Screenshot alınamadı: {e}")

        print("-" * 60)
        print(f"✓ Test tamamlandı: {self._testMethodName}\n")

    def run(self, result=None):
        """
        Test sonucunu yakalamak için override edildi
        """
        self._outcome = result
        return super().run(result)

    def test_send_message_with_free_model_and_verify_response(self):
        """
        Test: Ücretsiz modeli seç, mesaj gönder ve cevap doğrula

        Test Adımları:
        1. Ücretsiz GPT-5-Nano modelini seç
        2. Test mesajı yaz ve gönder
        3. Mesajın gönderildiğini doğrula
        4. AI cevabını bekle
        5. Cevap geldiğini doğrula (sayfa içeriği artışı)

        Beklenen Sonuç:
        - Model başarıyla seçilir
        - Mesaj başarıyla gönderilir
        - AI'dan cevap alınır
        """

        try:
            # ============ PART 1: MODEL SEÇİMİ ============
            print("\n" + "=" * 60)
            print("PART 1: ÜCRETSIZ MODEL SEÇİMİ")
            print("=" * 60)

            # Model seç
            model_selected = self.chat_page.select_model(Config.DEFAULT_MODEL)
            self.assertTrue(model_selected, f"{Config.DEFAULT_MODEL} modeli seçilemedi!")

            # Seçilen modeli doğrula
            current_model = self.chat_page.get_current_model()
            self.assertIsNotNone(current_model, "Model bilgisi alınamadı!")
            print(f"✅ Model seçimi başarılı: {current_model}\n")

            # ============ PART 2: MESAJ GÖNDERME ============
            print("=" * 60)
            print("PART 2: MESAJ GÖNDERME")
            print("=" * 60)

            test_message = Config.DEFAULT_MESSAGE

            # Mesaj göndermeden önce sayfa uzunluğunu kaydet
            page_source_before = self.chat_page.get_page_source()
            initial_length = len(page_source_before)
            print(f"📊 Mesaj öncesi sayfa uzunluğu: {initial_length} karakter\n")

            # Mesajı yaz
            self.chat_page.type_message(test_message)

            # Mesajın yazıldığını doğrula
            input_value = self.chat_page.get_message_input_value()
            self.assertIn("Merhaba", str(input_value),
                          "Mesaj input alanına yazılmadı!")

            # Mesajı gönder
            self.chat_page.click_send_button()

            # Mesajın gönderildiğini doğrula
            message_sent = self.chat_page.is_message_sent()
            self.assertTrue(message_sent,
                            "Mesaj gönderildikten sonra input alanı temizlenmedi!")

            # ============ PART 3: CEVAP DOĞRULAMA ============
            print("\n" + "=" * 60)
            print("PART 3: AI CEVABI DOĞRULAMA")
            print("=" * 60)

            # AI cevabını bekle
            self.chat_page.wait_for_response()

            # Sayfa içeriğinin değiştiğini kontrol et
            page_source_after = self.chat_page.get_page_source()
            final_length = len(page_source_after)
            print(f"📊 Cevap sonrası sayfa uzunluğu: {final_length} karakter")

            # Sayfa uzunluğunun arttığını doğrula
            length_increase = final_length - initial_length
            self.assertGreater(length_increase, 100,
                               f"Sayfa içeriği yeterince değişmedi! Artış: {length_increase} karakter")
            print(f"✅ Sayfa içeriği {length_increase} karakter arttı (cevap alındı)")

            # Ekran görüntüsü al
            screenshot_path = self.chat_page.take_screenshot('genie_final_test.png')
            print(f"📸 Ekran görüntüsü kaydedildi: {screenshot_path}")

            # Final assertion
            self.assertTrue(final_length > initial_length,
                            "AI'dan cevap gelmedi - sayfa içeriği değişmedi!")

            # ============ ÖZET ============
            print("\n" + "=" * 60)
            print("✅ TÜM ADIMLAR BAŞARIYLA TAMAMLANDI!")
            print("=" * 60)
            print(f"• Model: {Config.DEFAULT_MODEL} seçildi")
            print(f"• Mesaj: '{test_message}' gönderildi")
            print(f"• Cevap: {length_increase} karakter artış ile alındı")
            print("=" * 60)

        except AssertionError as e:
            # Assertion hatası durumunda screenshot al
            self._test_failed = True
            print(f"\n❌ Assertion Hatası: {e}")
            self.chat_page.take_screenshot_on_failure(self._testMethodName)
            raise  # Hatayı yeniden fırlat

        except Exception as e:
            # Diğer hatalar için screenshot al
            self._test_failed = True
            print(f"\n❌ Beklenmeyen Hata: {e}")
            self.chat_page.take_screenshot_on_failure(self._testMethodName)
            raise  # Hatayı yeniden fırlat


if __name__ == '__main__':
    # Test runner'ı yapılandır
    # Verbosity=2: Detaylı çıktı
    unittest.main(verbosity=2)