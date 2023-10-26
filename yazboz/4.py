import telepot

# Bot API anahtarınızı burada tanımlayın
TOKEN = '6825685191:AAEZapCvF64Q1Go8KfCRVAXQrfVBSVrX-j8'

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    # Eğer bir metin mesajıysa
    if content_type == 'text':
        # Gelen mesajın içeriğini alın
        message_text = msg['text']
        # Gelen mesajı ekrana yazdırın
        print(f"Mesaj: {message_text}")

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)

while True:
    # Programın çalışır durumda kalmasını sağlayın
    pass
