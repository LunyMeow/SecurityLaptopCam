# 📷 Python Güvenlik Kamerası Sistemi (Hareket Algılama + Email Gönderme)

Bu proje, OpenCV kullanarak hareket algılayan ve Flask ile canlı yayın sağlayan bir güvenlik kamerası uygulamasıdır. Hareket algılandığında belirlenen e-posta adreslerine anlık görüntü gönderir. Ayrıca canlı yayını tarayıcıdan izleyebilir ve bazı ayarları web arayüzünden değiştirebilirsiniz.

---

## 🔧 Özellikler

- ✅ Hareket algılama
- ✅ E-posta ile uyarı gönderme
- ✅ Flask ile canlı yayın
- ✅ Email gönderimini web arayüzünden aç/kapat
- ✅ Alıcı e-posta adreslerini web arayüzünden güncelleme
- ✅ "hesoyam" komutuyla görüntüyü dondur / çöz
- ✅ `.json` ile yapılandırılabilir ve dışarıdan dosya alır

---

## ⚙️ Yapılandırma

Aşağıdaki örneğe benzer bir `config.json` dosyası oluşturun:

```json
{
  "EMAIL_SENDER": "gonderen@gmail.com",
  "EMAIL_PASSWORD": "uygulama-sifresi",
  "EMAIL_RECEIVERS": [
    "alici1@example.com",
    "alici2@example.com"
  ]
}


## ▶️ Kullanım

### 1. Gerekli paketleri yükle

```bash
pip install opencv-python flask
```

### 2. Uygulamayı çalıştır

```bash
python main.py                 # config.json kullanır
python main.py ayarlar.json   # başka bir config dosyası kullan
```

### 3. Tarayıcıdan yayını izleyin

[http://localhost:8000](http://localhost:8000)

---

## 🖥️ Arayüz Özellikleri

* **Canlı Yayın:** Kameradan gelen görüntü anlık olarak gösterilir.
* **Email Gönderilsin mi?:** Checkbox ile mail gönderme aktif/pasif yapılabilir.
* **Alıcı Email Adresleri:** Güncellenebilir textarea. Satır satır adres girin.
* **Gönderilen Emailler:** Kime mail gönderildiği listelenir.
* **"hesoyam" komutu:** Yazınca görüntü dondurulur/çözülür.

---

## 📦 EXE'ye Dönüştürme (PyInstaller)

```bash
pyinstaller --onefile --add-data "config.json;." main.py
```

* `config.json` dosyasını exe'ye dahil eder.
* Exe çalışırken bu dosya yanında olmalıdır.

---

## 📝 Notlar

* Gmail ile kullanıyorsan, "uygulama şifresi" oluşturmalısın. (2 Adımlı doğrulama açık olmalı.)
* `motion.jpg` her tespit edilen harekette yeniden yazılır.

---


---

## 👤 Geliştirici

Bedirhan Alparslan
```


