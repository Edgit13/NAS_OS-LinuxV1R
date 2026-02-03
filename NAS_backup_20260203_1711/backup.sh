#!/bin/bash
BACKUP_DIR="$HOME/Documents/NAS_OS-LinuxV/shared_files"
ROOT_FREE=$(df / | awk 'NR==2 {print $4}') # в кілобайтах

# Якщо місця менше 2ГБ - скасовуємо бекап
if [ "$ROOT_FREE" -lt 2097152 ]; then
    echo "ПОМИЛКА: Мало місця на диску (менше 2ГБ)!"
    exit 1
fi

DATE=$(date +%Y%m%d_%H%M)
tar -czf "$BACKUP_DIR/NAS_backup_$DATE.tar.gz" -C "$HOME/Documents/NAS_OS-LinuxV" . --exclude="shared_files"
echo "Бекап створено успішно!"
