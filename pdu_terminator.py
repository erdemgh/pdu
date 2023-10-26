import platform
import subprocess
import time

def stop_pdu_processes():
  """Stops all running PDU processes."""

  process_list = subprocess.check_output(['ps', 'aux']).decode().split('\n')

  for line in process_list:
    if "pdu_" in line and ".py" in line:
      pid = line.split()[1]
      process_name = line.split()[-1]

      if platform.system() == "Windows":
        subprocess.run(["taskkill", "/f", "/t", "/im", process_name])
      else:
        subprocess.run(["kill", "-15", pid])

      try:
        subprocess.run(["kill", pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
      except subprocess.CalledProcessError:
        time.sleep(5)
        subprocess.run(["kill", "-9", pid])
        print(f"{process_name} (PID {pid}) süreci zorla sonlandırıldı.")

      print(f"{process_name} (PID {pid}) süreci sonlandırıldı.")

if __name__ == "__main__":
  stop_pdu_processes()
