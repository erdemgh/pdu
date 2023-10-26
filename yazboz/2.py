import telegram
import asyncio

# Telegram Bot token
bot_token = '6825685191:AAEZapCvF64Q1Go8KfCRVAXQrfVBSVrX-j8'
channel_id = '-4055301255'
# Flask ile iletişim kurmak için kullanacağımız URL
flask_url = 'http://127.0.0.1:2135/submit'  # Flask uygulamanızın URL'si



async def send_telegram_message(message):
    bot = telegram.Bot(token=bot_token)
    await bot.send_message(chat_id=channel_id, text=message)

async def main():
    while True:
        command = input("Mesajınızı girin (çıkmak için 'q' tuşuna basın): ")
        if command.lower() == 'q':
            break

        response = await send_command_to_flask(command)
        await send_telegram_message(response)

async def send_command_to_flask(command):
    import aiohttp
    data = {'command': command}
    async with aiohttp.ClientSession() as session:
        async with session.post(flask_url, data=data) as response:
            return await response.text()

if __name__ == '__main__':
    asyncio.run(main())
