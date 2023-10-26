import os
import subprocess
import re

tmp_cron_file = "/tmp/pdu_tmp_cron"

pdu_starter_path = os.path.abspath("pdu_starter.py")

delay_seconds = 69

proc = subprocess.Popen(['crontab', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = proc.communicate()
cron_content = stdout.decode()

new_cron_rule = f"@reboot sleep {delay_seconds} && python3 {pdu_starter_path}"

if re.search(rf"python3 {re.escape(pdu_starter_path)}", cron_content):
    cron_content = re.sub(rf"@reboot sleep \d+ && python3 {re.escape(pdu_starter_path)}\n", '', cron_content)

cron_content += new_cron_rule + '\n'

with open(tmp_cron_file, 'w') as f:
    f.write(cron_content)

subprocess.Popen(['crontab', tmp_cron_file])

print("Crontab kuralı başarıyla güncellendi.")
