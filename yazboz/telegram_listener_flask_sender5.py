import telepot
import requests

# Bot API anahtarınızı burada tanımlayın
TOKEN = '6825685191:AAEZapCvF64Q1Go8KfCRVAXQrfVBSVrX-j8'
FLASK_URL = 'http://127.0.0.1:2135/submit'  # Flask uygulamanızın URL'si

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    # Eğer bir metin mesajıysa
    if content_type == 'text':
        # Gelen mesajın içeriğini alın
        message_text = msg['text']
        # Gelen mesajı ekrana yazdırın
        print(f"Mesaj: {message_text}")
        # Gelen mesajı Flask uygulamanızı çağırmak için gönderin
        send_command_to_flask(message_text)

def send_command_to_flask(command):
    data = {'command': command}
    try:
        response = requests.post(FLASK_URL, data=data)
        response_text = response.text
        # Flask'tan gelen yanıtı ekrana yazdırabilir veya istediğiniz gibi işleyebilirsiniz
        print(f"Flask'tan Gelen Yanıt: {response_text}")
    except Exception as e:
        print(f"Flask'a komut gönderilirken bir hata oluştu: {str(e)}")

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)

while True:
    # Programın çalışır durumda kalmasını sağlayın
    pass
