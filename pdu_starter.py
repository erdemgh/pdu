import threading
import subprocess

def run_relay_controller_api_interface():
    subprocess.run(["python3", "relay_controller_api_interface.py"])

def run_telegram_bot():
    subprocess.run(["python3", "telegram_bot.py"])

if __name__ == "__main__":
    relay_controller_api_interface_thread = threading.Thread(target=run_relay_controller_api_interface)

    telegram_bot_thread = threading.Thread(target=run_telegram_bot)

    relay_controller_api_interface_thread.start()
    telegram_bot_thread.start()

    relay_controller_api_interface_thread.join()
    telegram_bot_thread.join()
