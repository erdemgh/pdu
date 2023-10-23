import serial
import time
from flask import Flask, render_template, request
import requests

ser = serial.Serial('/dev/ttyUSB0', 9600)

app = Flask(__name__)

# Fonksiyon telegram mesajı göndermek için ve içeriği ekrana yazdırmak için
def send_telegram_message(response):
    if response == "1":
        hostname = requests.get('http://169.254.169.254/latest/meta-data/hostname').text
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        message = f"""
Hostname: {hostname}
Enerji açıldı!

{timestamp}
"""

        print("Telegram Mesajı:")
        print(message)

        telegram_bot_api_token = '6825685191:AAEZapCvF64Q1Go8KfCRVAXQrfVBSVrX-j8'
        telegram_chat_id = '-4055301255'

        data = {
            'chat_id': telegram_chat_id,
            'text': message
        }

        response = requests.post(f'https://api.telegram.org/bot{telegram_bot_api_token}/sendMessage', data=data)

@app.route('/')
def index():
    return render_template('index3.html')  # index2.html kullan

@app.route('/submit', methods=['GET', 'POST'])  # Hem GET hem de POST isteklerini kabul et
def submit():
    if request.method == 'GET':
        command = request.args.get('command')  # GET ile gelen 'command' parametresini al
    elif request.method == 'POST':
        command = request.form['command']  # POST ile gelen 'command' parametresini al

    if command.lower() == 'q':
        return "Program sonlandırıldı."
    elif command == 'c':
        ser.write(command.encode())
        time.sleep(0.30)
        data = ser.readline()
        return data.decode()
    elif command in ['0', '1']:
        ser.write(command.encode())
        time.sleep(0.30)
        data = ser.readline()
        # Telegram mesajını gönder ve içeriği ekrana yazdır
        send_telegram_message(command)
        return data.decode()
    else:
        return "Geçersiz komut. Sadece '0', '1', 'c' veya 'q' kabul edilir."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2130)
