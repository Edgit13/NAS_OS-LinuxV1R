import socket
import json
import urllib.request
import urllib.parse
import os

CONFIG_PATH = "config.json"

def send_to_tg(text):
    print(f"--> Спроба відправки в TG: {text}", flush=True)
    if not os.path.exists(CONFIG_PATH):
        print(f"!!! Помилка: Файл {CONFIG_PATH} не знайдено всередині контейнера!", flush=True)
        return

    try:
        with open(CONFIG_PATH, 'r') as f:
            conf = json.load(f)
        
        token = conf.get("tg_token")
        chat_id = conf.get("tg_chat_id")

        if not token or not chat_id:
            print("!!! Помилка: В config.json порожній токен або ID", flush=True)
            return

        msg = urllib.parse.quote(text)
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}"
        
        with urllib.request.urlopen(url) as response:
            if response.getcode() == 200:
                print("✅ Успішно відправлено в Telegram!", flush=True)
            else:
                print(f"⚠️ Telegram повернув код: {response.getcode()}", flush=True)

    except Exception as e:
        print(f"❌ TG Error: {e}", flush=True)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    print("🚀 Месенджер активовано! Чекаю на порті 12345...", flush=True)

    while True:
        client, addr = server.accept()
        data = client.recv(1024).decode('utf-8').strip()
        if data:
            print(f"📥 Отримано: {data}", flush=True)
            send_to_tg(f"📟 NAS: {data}")
        client.close()

if __name__ == "__main__":
    start_server()
