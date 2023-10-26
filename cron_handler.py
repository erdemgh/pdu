import os
import subprocess

# pdu_starter.py'nin tam yolunu al
pdu_starter_path = os.path.abspath("pdu_starter.py")

# 69 saniye gecikme süresi
delay_seconds = 69

# Cron tabloyu oku
proc = subprocess.Popen(['crontab', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = proc.communicate()

# Crontab kuralını oluştur
cron_rule = f"{delay_seconds} * * * * sleep {delay_seconds} && python3 {pdu_starter_path}"

# Crontab kuralının zaten mevcut olup olmadığını kontrol et
if cron_rule in stdout.decode():
    print("Kayıt mevcut ve güncel")
else:
    # Yeni crontab kuralını ekle
    with open('tmp_cron', 'w') as f:
        f.write(stdout.decode())
        f.write(cron_rule)

    # Yeni crontab'ı yükle
    subprocess.Popen(['crontab', 'tmp_cron'])
    os.remove('tmp_cron')

print("Crontab kuralı başarıyla güncellendi.")
