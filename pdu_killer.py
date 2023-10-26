import subprocess

def stop_pdu_processes():
    process_list = subprocess.check_output(['ps', 'aux']).decode().split('\n')
    for line in process_list:
        if "pdu_" in line:
            pid = line.split()[1]
            process_name = line.split()[-1]
            subprocess.run(['kill', '-9', pid])
            print(f"{process_name} (PID {pid}) süreci sonlandırıldı.")

if __name__ == "__main__":
    stop_pdu_processes()
