import telepot
import requests
import socket
import datetime

TOKEN = '6825685191:AAEZapCvF64Q1Go8KfCRVAXQrfVBSVrX-j8'
FLASK_URL = 'http://127.0.0.1:2135/submit'
CHANNEL_ID = '-4055301255'

bot = telepot.Bot(TOKEN)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        message_text = msg['text']
        response_text = send_command_to_flask(message_text)
        send_response_to_channel(message_text, response_text)


def send_command_to_flask(command):
    data = {'command': command}
    try:
        response = requests.post(FLASK_URL, data=data)
        response_text = response.text
        return response_text
    except Exception as e:
        print(f"Flask'a komut gönderilirken bir hata oluştu: {str(e)}")
        return "Hata oluştu: Flask'a komut gönderilemedi"


def send_response_to_channel(message_text, response_text):
    machine_name = socket.gethostname()
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"{machine_name} / {current_time}\nMesaj: {message_text}\nYanit: {response_text}"

    print(message)
    bot.sendMessage(CHANNEL_ID, message)


bot.message_loop(handle)

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Program sonlandırıldı.")
