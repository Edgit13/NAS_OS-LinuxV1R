import time
import socket
import os

LOG_FILE = "server_log.txt"
MSG_PORT = 12345
TEMP_LIMIT = 70.0

def send_to_messenger(text):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect(('127.0.0.1', MSG_PORT))
            s.sendall(text.encode('utf-8'))
    except:
        pass

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return int(f.read().strip()) / 1000
    except:
        return 0

def monitor():
    # Початкове сповіщення без емодзі для логів терміналу
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'a').close()

    with open(LOG_FILE, 'r') as f:
        f.seek(0, os.SEEK_END)
        
        while True:
            current_temp = get_cpu_temp()
            if current_temp > TEMP_LIMIT:
                send_to_messenger(f"⚠️ Warning: CPU {current_temp}C")
            
            line = f.readline()
            if line:
                if "PUT" in line:
                    send_to_messenger(f"📥 Upload: {line.strip()}")
                elif "DELETE" in line:
                    send_to_messenger(f"🗑️ Delete: {line.strip()}")
            
            time.sleep(1)

if __name__ == "__main__":
    monitor()
