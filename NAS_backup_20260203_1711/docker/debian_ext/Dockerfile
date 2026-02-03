FROM debian:stable-slim

# Встановлюємо залежності (python для месенджера)
RUN apt-get update && apt-get install -y python3 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копіюємо код месенджера
COPY app_code/messenger.py .

# Запускаємо з прапором -u для миттєвих логів
CMD ["python3", "-u", "messenger.py"]
