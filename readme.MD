# GenieChat iOS Appium Test Automation

Bu proje, GenieChat iOS uygulamasi icin Appium kullanarak yazilmis otomasyon test framework'udur. Page Object Model (POM) pattern'i ile gelistirilmistir.

## Ozellikler

- Page Object Model (POM) tasarim deseni
- unittest framework kullanimi
- iOS cihaz uzerinde test destegi
- AI model secimi otomasyonu
- Mesaj gonderme ve cevap dogrulama
- Ekran goruntusu alma
- Detayli raporlama

## Gereksinimler

### Yazilimlar
- Python 3.8+
- Xcode 12.0+
- Appium 2.x
- iOS cihaz (fiziksel)
- macOS (iOS testleri icin zorunlu)

### Python Paketleri
```bash
pip install appium-python-client
pip install selenium
```

## Kurulum

### 1. Appium Kurulumu

```bash
npm install -g appium
appium driver install xcuitest
```

### 2. WebDriverAgent Imzalama

WebDriverAgent'i Xcode ile imzalamaniz gerekiyor:

```bash
cd ~/.appium/node_modules/appium-xcuitest-driver/node_modules/appium-webdriveragent
open WebDriverAgent.xcodeproj
```

Xcode'da:
1. WebDriverAgentRunner ve WebDriverAgentLib target'larini secin
2. Signing & Capabilities sekmesinde:
   - Automatically manage signing
   - Team: Apple ID'nizi secin
   - Bundle Identifier'i degistirin: com.yourname.WebDriverAgentRunner

### 3. iOS Cihaz Hazirligi

1. Ayarlar > Gizlilik ve Guvenlik > Gelistirici Modu -> Ac
2. UDID'nizi alin:
```bash
idevice_id -l
```
3. utils/config.py dosyasinda UDID'nizi guncelleyin

### 4. Gelistirici Guveni

Ilk test calistirmasindan sonra:
- Ayarlar > Genel > VPN ve Cihaz Yonetimi
- Apple ID'nize guven verin

## Kullanim

### Appium Sunucusunu Baslatma

```bash
appium
```

Server varsayilan olarak http://127.0.0.1:4723 adresinde calisir.

### Testleri Calistirma

```bash
cd "App Case/tests"
python test_genie_chat_main_flow.py
```

veya unittest ile:

```bash
python -m unittest test_genie_chat_main_flow.py -v
```

## Proje Yapisi

```
App Case/
├── pages/
│   ├── base_page.py          # Temel page object sinifi
│   └── chat_page.py           # Chat sayfasi metodlari
├── tests/
│   └── test_genie_chat_main_flow.py  # Ana test senaryosu
└── utils/
    ├── config.py              # Test konfigurasyonu
    └── driver_factory.py      # Appium driver yonetimi
```

## Test Senaryosu

### test_send_message_with_free_model_and_verify_response

Amac: Ucretsiz AI modeli ile mesaj gonderme ve cevap alma testi

Adimlar:
1. GenieChat uygulamasini ac
2. Ucretsiz GPT-5-Nano modelini sec
3. "Merhaba, nasilsin?" mesajini yaz ve gonder
4. Mesajin gonderildigini dogrula
5. AI'dan cevap geldigini dogrula (AI mesaj kutusunun varligini kontrol et)
6. Ekran goruntusu al

Beklenen Sonuc: Mesaj basariyla gonderilir ve AI'dan cevap alinir

### Ornek Test Kaydi

Test senaryosunun calisirken kaydedilmis videosunu izlemek icin:

[Test Kaydi Videosu](https://drive.google.com/file/d/1XM8hYBDVdtMaJ4bUFgajt8MAdWyOZmJE/view?usp=sharing)

## Yapilandirma

utils/config.py dosyasinda test ayarlarini duzenleyebilirsiniz:

```python
class Config:
    PLATFORM_NAME = 'iOS'
    DEVICE_NAME = 'iPhone'
    UDID = '00008110-000965D61402601E'  # Kendi UDID'nizi girin
    BUNDLE_ID = 'co.appnation.geniechat'
    AUTOMATION_NAME = 'XCUITest'
    NO_RESET = True
    APPIUM_SERVER = 'http://127.0.0.1:4723'

    DEFAULT_MODEL = 'GPT-5 Nano'
    DEFAULT_MESSAGE = 'Merhaba, nasilsin?'
    AI_RESPONSE_WAIT_TIME = 15
```

## Sorun Giderme

### Appium baglanamıyor
```bash
appium
appium driver list
```

### WebDriverAgent imzalama hatasi
- Xcode'da Bundle Identifier'i benzersiz yapin
- Team secimini kontrol edin
- iOS cihazda gelistirici guveni verdiginizden emin olun

### Element bulunamiyor
- Appium Inspector ile elementleri kontrol edin
- config.py'daki bekleme surelerini artirin
- Uygulama versiyonunun degisip degismedigini kontrol edin

### Test basarisiz oluyor
- UDID'nin dogru oldugunu kontrol edin
- Bundle ID'nin dogru oldugunu kontrol edin
- iOS cihazin Developer Mode acik olmali
- GenieChat uygulamasinin cihazda yuklu oldugunu dogrulayin

## Hata Ayiklama

### Ekran Goruntuleri

Testler basarisiz oldugunda otomatik olarak screenshot alinir:
- error_<test_name>_<timestamp>.png
- genie_final_test.png