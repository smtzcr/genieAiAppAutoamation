# GenieChat iOS Appium Test Automation

Bu proje, GenieChat iOS uygulaması için Appium kullanarak yazılmış otomasyon test framework'üdür. Page Object Model (POM) pattern'ı ile geliştirilmiştir.

## 📋 Özellikler

- ✅ Page Object Model (POM) tasarım deseni
- ✅ unittest framework kullanımı
- ✅ iOS cihaz üzerinde test desteği
- ✅ AI model seçimi otomasyonu
- ✅ Mesaj gönderme ve cevap doğrulama
- ✅ Ekran görüntüsü alma
- ✅ Detaylı raporlama

## 🛠 Gereksinimler

### Yazılımlar
- Python 3.8+
- Xcode 12.0+
- Appium 2.x
- iOS cihaz (fiziksel)
- macOS (iOS testleri için zorunlu)

### Python Paketleri
```bash
pip install -r requirements.txt
```

## 📦 Kurulum

### 1. Appium Kurulumu

```bash
# Homebrew ile Appium
brew install appium

# XCUITest driver
appium driver install xcuitest@7.35.0
```

### 2. WebDriverAgent İmzalama

WebDriverAgent'ı Xcode ile imzalamanız gerekiyor:

```bash
cd ~/.appium/node_modules/appium-xcuitest-driver/node_modules/appium-webdriveragent
open WebDriverAgent.xcodeproj
```

Xcode'da:
1. **WebDriverAgentRunner** ve **WebDriverAgentLib** target'larını seçin
2. **Signing & Capabilities** sekmesinde:
   - ☑️ Automatically manage signing
   - Team: Apple ID'nizi seçin
   - Bundle Identifier'ı değiştirin: `com.yourname.WebDriverAgentRunner`

### 3. iOS Cihaz Hazırlığı

1. **Ayarlar** > **Gizlilik ve Güvenlik** > **Geliştirici Modu** → Aç
2. UDID'nizi alın:
```bash
idevice_id -l
```
3. `config/config.py` dosyasında UDID'nizi güncelleyin

### 4. Geliştirici Güveni

İlk test çalıştırmasından sonra:
- **Ayarlar** > **Genel** > **VPN ve Cihaz Yönetimi**
- Apple ID'nize güven verin

### 5. Proje Kurulumu

```bash
# Projeyi klonlayın veya indirin
cd genie_appium_tests

# Sanal ortam oluşturun (opsiyonel ama önerilir)
python3 -m venv venv
source venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

## 🚀 Kullanım

### Appium Sunucusunu Başlatma

```bash
# Terminal 1
appium
```

### Testleri Çalıştırma

```bash
# Terminal 2 - Tüm testleri çalıştır
python3 -m unittest discover -s tests -v

# Belirli bir test çalıştır
python3 -m unittest tests.test_genie_chat.GenieChatiOSTest.test_send_message_with_free_model_and_verify_response -v

# Kısa yol
cd tests
python3 test_genie_chat.py
```

## 📁 Proje Yapısı

```
genie_appium_tests/
│
├── README.md                          # Bu dosya
├── requirements.txt                   # Python bağımlılıkları
│
├── config/                            # Konfigürasyon
│   ├── __init__.py
│   └── config.py                      # Test ayarları (UDID, bundle ID, vb.)
│
├── pages/                             # Page Object sınıfları
│   ├── __init__.py
│   ├── base_page.py                   # Temel page sınıfı
│   └── genie_chat_page.py             # GenieChat sayfası
│
├── tests/                             # Test dosyaları
│   ├── __init__.py
│   └── test_genie_chat.py             # GenieChat test senaryoları
│
└── utils/                             # Yardımcı fonksiyonlar
    ├── __init__.py
    └── driver_factory.py              # Appium driver factory
```

## 🧪 Test Senaryoları

### test_send_message_with_free_model_and_verify_response

**Amaç:** Ücretsiz AI modeli ile mesaj gönderme ve cevap alma testi

**Adımlar:**
1. GenieChat uygulamasını aç
2. Ücretsiz GPT-5-Nano modelini seç
3. "Merhaba, nasılsın?" mesajını yaz ve gönder
4. Mesajın gönderildiğini doğrula
5. AI'dan cevap geldiğini doğrula (sayfa içeriği artışı)
6. Ekran görüntüsü al

**Beklenen Sonuç:** Mesaj başarıyla gönderilir ve AI'dan cevap alınır

## 🔧 Yapılandırma

### config/config.py

Test ayarlarını bu dosyada düzenleyebilirsiniz:

```python
class Config:
    PLATFORM_NAME = 'iOS'
    DEVICE_NAME = 'iPhone'
    UDID = '00008110-000965D61402601E'  # Kendi UDID'nizi girin
    BUNDLE_ID = 'co.appnation.geniechat'
    AUTOMATION_NAME = 'XCUITest'
    NO_RESET = True
    APPIUM_SERVER = 'http://127.0.0.1:4723'
```

## 📊 Test Çıktısı

Test çalıştırıldığında detaylı log çıktısı alırsınız:

```
============================================================
🚀 Test sınıfı başlatılıyor...
============================================================
✅ Appium bağlantısı kuruldu

test_send_message_with_free_model_and_verify_response ...
▶️  Test başlıyor: test_send_message_with_free_model_and_verify_response
------------------------------------------------------------

============================================================
PART 1: ÜCRETSIZ MODEL SEÇİMİ
============================================================
🤖 Model dropdown açılıyor...
📊 Şu anki model: DeepSeek
✅ Model dropdown açıldı
🔍 'GPT-5-Nano' aranıyor...
⌨️  'GPT-5-Nano' yazılıyor...
✅ Arama tamamlandı
🎯 'GPT-5-Nano' seçiliyor...
✅ 'GPT-5-Nano' seçildi!
📊 Yeni seçilen model: GPT-5-Nano
✅ Model seçimi başarılı: GPT-5-Nano

============================================================
PART 2: MESAJ GÖNDERME
============================================================
📊 Mesaj öncesi sayfa uzunluğu: 4532 karakter
📝 Mesaj yazılıyor: 'Merhaba, nasılsın?'
✅ Mesaj yazıldı
📤 Mesaj gönderiliyor...
✅ Gönder butonuna basıldı
✅ Input alanı temizlendi (mesaj gönderildi)

============================================================
PART 3: AI CEVABI DOĞRULAMA
============================================================
⏳ AI'dan cevap bekleniyor (15 saniye)...
📊 Cevap sonrası sayfa uzunluğu: 7891 karakter
✅ Sayfa içeriği 3359 karakter arttı (cevap alındı)
📸 Ekran görüntüsü kaydedildi: genie_final_test.png

============================================================
✅ TÜM ADIMLAR BAŞARIYLA TAMAMLANDI!
============================================================
• Model: GPT-5-Nano seçildi
• Mesaj: 'Merhaba, nasılsın?' gönderildi
• Cevap: 3359 karakter artış ile alındı
============================================================

ok
----------------------------------------------------------------------
Ran 1 test in 45.234s

OK
```

## 🐛 Sorun Giderme

### Appium bağlanamıyor
```bash
# Appium'un çalıştığından emin olun
appium

# Driver'ların yüklü olduğunu kontrol edin
appium driver list
```

### WebDriverAgent imzalama hatası
- Xcode'da Bundle Identifier'ı benzersiz yapın
- Team seçimini kontrol edin
- iOS cihazda geliştirici güveni verdiğinizden emin olun

### Element bulunamıyor
- Appium Inspector ile elementleri kontrol edin
- `config.py`'daki bekleme sürelerini artırın
- Uygulama versiyonunun değişip değişmediğini kontrol edin

### Test başarısız oluyor
- UDID'nin doğru olduğundan emin olun
- Bundle ID'nin doğru olduğundan emin olun
- iOS cihazın Developer Mode açık olmalı

## 📝 Yeni Test Ekleme

1. `pages/` klasöründe yeni bir page object oluşturun (gerekirse)
2. `tests/` klasöründe yeni test dosyası ekleyin
3. unittest.TestCase'den türetin
4. Test metodunu yazın (method adı `test_` ile başlamalı)

Örnek:
```python
def test_new_feature(self):
    """Yeni özellik testi"""
    self.chat_page.some_new_method()
    self.assertTrue(result)
```

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje eğitim amaçlı oluşturulmuştur.

## 📧 İletişim

Sorularınız için issue açabilirsiniz.

## 🔗 Faydalı Linkler

- [Appium Documentation](http://appium.io/docs/en/latest/)
- [Appium Python Client](https://github.com/appium/python-client)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [Page Object Model](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)