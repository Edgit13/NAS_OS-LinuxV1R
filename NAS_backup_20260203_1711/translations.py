# Language translations for NAS OS

TRANSLATIONS = {
    "uk": {
        # Menu items
        "toggle_dufs": "Увімкнути/Вимкнути DUFS сервер",
        "toggle_web": "Увімкнути/Вимкнути Веб-меню",
        "toggle_msg": "Увімкнути/Вимкнути Debian Messenger (Docker)",
        "disk_info": "Інформація про диски",
        "system_info": "Системна інформація",
        "settings": "Налаштування",
        "exit": "Вихід",
        "main_menu": "Головне меню",
        
        # Status
        "status": "Статус",
        "auto_refresh": "Авто-оновлення: 5 сек",
        "booting": "Завантаження...",
        "goodbye": "До побачення!",
        
        # Actions
        "web_stopped": "ЗУПИНЕНО",
        "web_started": "ЗАПУЩЕНО",
        "press_enter": "Натисніть Enter...",
        "press_enter_return": "Натисніть Enter щоб повернутися...",
        
        # System info
        "sys_info_title": "СИСТЕМНА ІНФОРМАЦІЯ",
        "ip_address": "IP адреса:",
        "uptime": "Час роботи:",
        "running_services": "ЗАПУЩЕНІ СЕРВІСИ",
        "dufs_server": "DUFS сервер",
        "web_menu": "Веб-меню",
        "terminal_menu": "Термінальне меню",
        "currently_running": "зараз працює",
        "not_running": "не запущено",
        "memory": "ПАМ'ЯТЬ",
        "cpu_temp": "Температура CPU:",
        
        # Disk info
        "disk_info_title": "ІНФОРМАЦІЯ ПРО ДИСКИ",
        "disk_usage": "ВИКОРИСТАННЯ",
        
        # Settings
        "settings_title": "НАЛАШТУВАННЯ",
        "language": "Мова інтерфейсу",
        "select_language": "Виберіть мову:",
        "ukrainian": "Українська",
        "english": "English",
        "theme_color": "Колір теми",
        "os_name": "Назва системи",
        "save_settings": "Зберегти налаштування",
        "settings_saved": "Налаштування збережено!",
        "back": "Назад",
        
        # Telegram setup
        "tg_setup": "Налаштування Telegram",
        "tg_token_label": "Токен API:",
        "tg_id_label": "Ваш Chat ID:",
        "tg_saved": "Дані Telegram збережено!"
    },
    
    "en": {
        # Menu items
        "toggle_dufs": "Toggle DUFS Server",
        "toggle_web": "Toggle Web Menu",
        "toggle_msg": "Toggle Debian Messenger (Docker)",
        "disk_info": "Disk Information",
        "system_info": "System Information",
        "settings": "Settings",
        "exit": "Exit",
        "main_menu": "Main Menu",
        
        # Status
        "status": "Status",
        "auto_refresh": "Auto-refresh: 5 sec",
        "booting": "Booting...",
        "goodbye": "Goodbye!",
        
        # Actions
        "web_stopped": "STOPPED",
        "web_started": "STARTED",
        "press_enter": "Press Enter...",
        "press_enter_return": "Press Enter to return...",
        
        # System info
        "sys_info_title": "SYSTEM INFORMATION",
        "ip_address": "IP Address:",
        "uptime": "Uptime:",
        "running_services": "RUNNING SERVICES",
        "dufs_server": "DUFS Server",
        "web_menu": "Web Menu",
        "terminal_menu": "Terminal Menu",
        "currently_running": "currently running",
        "not_running": "not running",
        "memory": "MEMORY",
        "cpu_temp": "CPU Temperature:",
        
        # Disk info
        "disk_info_title": "DISK INFORMATION",
        "disk_usage": "USAGE",
        
        # Settings
        "settings_title": "SETTINGS",
        "language": "Interface Language",
        "select_language": "Select language:",
        "ukrainian": "Українська",
        "english": "English",
        "theme_color": "Theme Color",
        "os_name": "System Name",
        "save_settings": "Save Settings",
        "settings_saved": "Settings saved!",
        "back": "Back",

        # Telegram setup
        "tg_setup": "Telegram Settings",
        "tg_token_label": "API Token:",
        "tg_id_label": "Your Chat ID:",
        "tg_saved": "Telegram data saved!"
    }
}

def get_text(key, lang="uk"):
    """Get translated text"""
    return TRANSLATIONS.get(lang, TRANSLATIONS["uk"]).get(key, key)
