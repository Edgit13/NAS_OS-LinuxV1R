#!/bin/bash

BINARY="./bin/dufs"
ROOT_DIR="./shared_files"
PORT=5000

# Створюємо папку для файлів
mkdir -p "$ROOT_DIR"

# Перевіряємо чи процес уже запущений
PID=$(pgrep -f "$BINARY")

if [ -z "$PID" ]; then
    echo "INITIATING DUFS SERVER START..."
    
    # Запуск DUFS на порту 5000 з повним доступом
    "$BINARY" "$ROOT_DIR" -p "$PORT" -A > server_log.txt 2>&1 &
    
    sleep 1
    if pgrep -f "$BINARY" > /dev/null; then
        echo "SUCCESS: DUFS SERVER IS LIVE ON PORT $PORT"
        echo "Access at: http://$(hostname -I | awk '{print $1}'):$PORT"
    else
        echo "ERROR: DUFS STARTUP FAILED"
        cat server_log.txt
    fi
else
    echo "INITIATING DUFS SHUTDOWN..."
    kill "$PID"
    sleep 1
    echo "SUCCESS: DUFS SERVER HALTED"
fi
