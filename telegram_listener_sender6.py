import telepot
import requests

# Bot API anahtarınızı burada tanımlayın
TOKEN = '6825685191:AAEZapCvF64Q1Go8KfCRVAXQrfVBSVrX-j8'
FLASK_URL = 'http://127.0.0.1:2135/submit'  # Flask uygulamanızın URL'si
CHANNEL_ID = '-4055301255'

bot = telepot.Bot(TOKEN)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    # Eğer bir metin mesajıysa
    if content_type == 'text':
        # Gelen mesajın içeriğini alın
        message_text = msg['text']
        # Gelen mesajı ekrana yazdırın
        # print(f"Mesaj: {message_text}")
        # Gelen mesajı Flask uygulamanızı çağırmak için gönderin
        response_text = send_command_to_flask(message_text)
        # Yanıtı hedef kanala gönderin
        send_response_to_channel(message_text, response_text)

def send_command_to_flask(command):
    data = {'command': command}
    try:
        response = requests.post(FLASK_URL, data=data)
        response_text = response.text
        # Flask'tan gelen yanıtı döndürün
        return response_text
    except Exception as e:
        print(f"Flask'a komut gönderilirken bir hata oluştu: {str(e)}")
        return "Hata oluştu: Flask'a komut gönderilemedi"

def send_response_to_channel(message_text, response_text):
    # Hedef kanala yanıtı gönderin
    print(f"Mesaj: {message_text}")
    print(f"Yanit: {response_text}")
    bot.sendMessage(CHANNEL_ID, f"Mesaj: {message_text}")
    bot.sendMessage(CHANNEL_ID, f"Yanit: {response_text}")


bot.message_loop(handle)

# Sonsuz bir döngü yerine programın çalışır durumda kalmasını sağlayacak bir yöntem kullanabilirsiniz.
# Örneğin, Ctrl+C tuşlarına basarak programı sonlandırabilirsiniz.
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Program sonlandırıldı.")
