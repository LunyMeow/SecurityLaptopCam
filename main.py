import cv2
import smtplib
import ssl
from email.message import EmailMessage
import time
from flask import Flask, Response, render_template_string
import threading
import json
import os


# config.json dosyasını oku
with open("config.json", "r") as config_file:
    config = json.load(config_file)

EMAIL_SENDER = config.get("EMAIL_SENDER")
EMAIL_PASSWORD = config.get("EMAIL_PASSWORD")
EMAIL_RECEIVERS = config.get("EMAIL_RECEIVERS", [])


cap = cv2.VideoCapture(0)
time.sleep(2)

app = Flask(__name__)
last_sent_time = 0
latest_frame = None
freeze_frame = False  # dondurma durumu
frozen_image = None
email_thread = None  # en başta tanımlanmalı

HTML_MAIN = """
<!DOCTYPE html>
<html>
<head>
    <title>Güvenlik Kamerası</title>
    <style>
        body { text-align: center; font-family: Arial; margin-top: 50px; }
        button { font-size: 18px; padding: 10px 20px; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>📷 Güvenlik Kamerasına Hoş Geldiniz!</h1>
    <button onclick="window.location.href='/video'">Canlı Yayını İzle</button>
</body>
</html>
"""

HTML_VIDEO = """
<!DOCTYPE html>
<html>
<head>
    <title>Canlı Yayın</title>
    <style>
        body {
            text-align: center;
            font-family: Arial;
            background: #111;
            color: white;
        }
        img {
            margin-top: 20px;
            border: 5px solid #555;
        }
        input {
            margin-top: 20px;
            padding: 10px;
            font-size: 16px;
            border-radius: 5px;
            border: none;
            width: 200px;
        }
    </style>
</head>
<body>
    <h1>🎥 Canlı Yayın</h1>
    
    <input type="text" id="secretInput" placeholder="">

    <img src="{{ url_for('video_feed') }}" width="640" height="480" id="video">

    <script>
        const inputBox = document.getElementById('secretInput');

        inputBox.addEventListener('input', function() {
            if (inputBox.value.toLowerCase().trim() === 'hesoyam') {
                fetch('/toggle_freeze');  // Sunucuya komut gönder
                inputBox.value = '';      // Girdiyi temizle
            }
        });
    </script>
</body>
</html>

"""

def send_email(image_path):
    if freeze_frame:
        print("Görüntü donduruldu. Mail gönderilmiyor.")
        return
      # mail istemiyorsan bu satır kalsın
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Hareket Algılandı!'
        msg['From'] = EMAIL_SENDER
        msg['To'] = ', '.join(EMAIL_RECEIVERS)
        msg.set_content('Kamerada hareket algılandı. Ekteki görüntüye bak.')

        with open(image_path, 'rb') as f:
            img_data = f.read()
            msg.add_attachment(img_data, maintype='image', subtype='jpeg', filename='motion.jpg')

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("📧 Mail gönderildi.")
    except Exception as e:
        print(f"Mail gönderilirken hata oluştu: {e}")

def motion_detection():
    global last_sent_time, latest_frame, freeze_frame, frozen_image,email_thread
    frame1 = cap.read()[1]
    frame2 = cap.read()[1]

    while True:
        success, frame = cap.read()
        if not success:
            continue

        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False

        for contour in contours:
            if cv2.contourArea(contour) < 1000:
                continue
            motion_detected = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if motion_detected:
            current_time = time.time()
            if current_time - last_sent_time >= 10:
                if email_thread is None or not email_thread.is_alive():
                    cv2.imwrite('motion.jpg', frame1)
                    print("🎯 Hareket algılandı! Mail gönderiliyor...")
                    email_thread = threading.Thread(target=send_email, args=('motion.jpg',), daemon=True)
                    email_thread.start()
                    last_sent_time = current_time

        if not freeze_frame:
            latest_frame = frame1.copy()
        else:
            if frozen_image is None:
                frozen_image = frame1.copy()
            latest_frame = frozen_image

        frame1 = frame2
        frame2 = frame

def generate_frames():
    global latest_frame
    while True:
        if latest_frame is None:
            continue
            
        ret, buffer = cv2.imencode('.jpg', latest_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template_string(HTML_MAIN)

@app.route('/video')
def video_page():
    return render_template_string(HTML_VIDEO)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/toggle_freeze')
def toggle_freeze():
    global freeze_frame, frozen_image
    freeze_frame = not freeze_frame
    if not freeze_frame:
        frozen_image = None
    print(f"🎮 Freeze modu: {'DONDURULDU' if freeze_frame else 'CANLI'}")
    return ('', 204)  # boş yanıt

if __name__ == "__main__":
    threading.Thread(target=motion_detection, daemon=True).start()
    app.run(host='0.0.0.0', port=8000)
