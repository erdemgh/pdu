import telegram
import asyncio

telegram_token = '6825685191:AAEZapCvF64Q1Go8KfCRVAXQrfVBSVrX-j8'
telegram_channel_id = '-4055301255'
telegram_message = 'Merhaba, Dünya!'

async def send_telegram_message(telegram_token, telegram_channel_id, telegram_message):
    bot = telegram.Bot(token=telegram_token)
    await bot.send_message(chat_id=telegram_channel_id, text=telegram_message)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_telegram_message(telegram_token, telegram_channel_id, telegram_message))

