import threading
import subprocess

usage = "permanent"  # permanent ise crontab'a görev ekler, "temporary" ise crontab'daki absolute pathli kuralı siler.

def run_cron_handler():
    subprocess.run(["python3", "cron_handler.py", usage])

def run_relay_controller_api_interface():
    subprocess.run(["python3", "relay_controller_api_interface.py"])

def run_telegram_bot():
    subprocess.run(["python3", "telegram_bot.py"])

if __name__ == "__main__":
    cron_handler_thread = threading.Thread(target=run_cron_handler)
    relay_controller_api_interface_thread = threading.Thread(target=run_relay_controller_api_interface)
    telegram_bot_thread = threading.Thread(target=run_telegram_bot)

    cron_handler_thread.start()
    cron_handler_thread.join()

    relay_controller_api_interface_thread.start()
    telegram_bot_thread.start()

    relay_controller_api_interface_thread.join()
    telegram_bot_thread.join()
