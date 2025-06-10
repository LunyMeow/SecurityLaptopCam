Tabii! İşte hem İngilizce hem Türkçe açıklamalı, bu projeye uygun örnek bir **README.md** dosyası:

````markdown
# Security Laptop Camera / Güvenlik Laptop Kamerası

---

## English

This project is a simple security camera system with motion detection and live video streaming via a Flask web server.  
When motion is detected, it sends an email with a snapshot. There is also a "freeze" feature activated by typing a secret word in the web interface.

### Features

- Live camera streaming on a web page
- Motion detection with bounding boxes
- Email alerts with a captured image when motion occurs
- Freeze/unfreeze live video by entering a secret code (`hesoyam`) on the webpage

### Requirements

- Python 3.x
- OpenCV (`opencv-python`)
- Flask
- Email account (e.g., Gmail) with SMTP enabled
- `config.json` file with email credentials and recipients

### Setup

1. Install dependencies:

```bash
pip install opencv-python flask
````

2. Create a `config.json` file in the project directory with the following structure:

```json
{
  "EMAIL_SENDER": "your_email@gmail.com",
  "EMAIL_PASSWORD": "your_email_password_or_app_password",
  "EMAIL_RECEIVERS": ["receiver1@example.com", "receiver2@example.com"]
}
```

3. Run the script:

```bash
python main.py
```

4. Open your browser and go to:

```
http://localhost:8000/
```

### Usage

* Click **"Canlı Yayını İzle"** on the main page to watch the live video feed.
* In the live feed page, type **hesoyam** in the input box to freeze/unfreeze the video.
* When motion is detected, an email with an image attachment will be sent to the configured recipients (every 10 seconds at most).

---

## Türkçe

Bu proje, hareket algılama ve canlı video yayını yapan basit bir güvenlik kamerası sistemidir.
Hareket algılandığında, anlık görüntü e-posta ile gönderilir. Ayrıca, web arayüzündeki gizli kelime girildiğinde videoyu dondurma/çözme özelliği vardır.

### Özellikler

* Web sayfasında canlı kamera yayını
* Hareket algılama ve hareket alanına kutu çizme
* Hareket olduğunda e-posta bildirimi ve ekli görüntü gönderimi
* Web sayfasındaki gizli kelime (`hesoyam`) ile videoyu dondurma ve çözme

### Gereksinimler

* Python 3.x
* OpenCV (`opencv-python`)
* Flask
* SMTP etkinleştirilmiş bir e-posta hesabı (örneğin Gmail)
* E-posta bilgileri ve alıcıların yazıldığı `config.json` dosyası

### Kurulum

1. Gerekli paketleri yükleyin:

```bash
pip install opencv-python flask
```

2. Proje klasörüne aşağıdaki gibi bir `config.json` dosyası oluşturun:

```json
{
  "EMAIL_SENDER": "sizin_email@gmail.com",
  "EMAIL_PASSWORD": "email_sifreniz_veya_uygulama_sifresi",
  "EMAIL_RECEIVERS": ["alici1@example.com", "alici2@example.com"]
}
```

3. Scripti çalıştırın:

```bash
python main.py
```

4. Tarayıcınızda şu adresi açın:

```
http://localhost:8000/
```

### Kullanım

* Ana sayfadaki **"Canlı Yayını İzle"** butonuna tıklayarak canlı görüntüyü izleyin.
* Canlı yayın sayfasındaki metin kutusuna **hesoyam** yazıp enter tuşuna basmadan bekleyin; video dondurulur veya çözülür.
* Hareket algılandığında, 10 saniyede bir en fazla olacak şekilde, ayarlanan alıcılara e-posta ile anlık görüntü gönderilir.

---

