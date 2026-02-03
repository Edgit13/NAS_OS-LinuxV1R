```markdown
# 🚀 NAS_OS-LinuxV 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Linux](https://img.shields.io/badge/platform-linux-lightgrey.svg)](https://kernel.org)

An all-in-one, lightweight NAS management solution. Features a terminal UI, web management interface, and real-time Telegram notifications via Docker-based monitoring.

---

## 📥 Installation

1. **Download the Archive**:  
   Download the latest `NAS_backup_XXXX.tar.gz` from the repository.
   
2. **Extract & Navigate**:
   ```bash
   tar -xzf NAS_backup_*.tar.gz
   cd NAS_backup_XXXX

```

3. **Launch the System**:
Run the starter script to open the main menu:
```bash
./starter.sh

```


> **💡 Troubleshooting**: If you get `Permission denied`, run:
> `chmod +x starter.sh`



---

## 🤖 Telegram Integration Setup

Stay updated with your system status by connecting your Telegram account.

1. **Get your Chat ID**:
Open Telegram and message [@userinfobot](https://t.me/userinfobot) to receive your unique numeric ID.
2. **Configure the NAS OS**:
* In the main menu, press `6` (**Settings**) and hit **Enter**.
* Press `2` (**Telegram ID**) and hit **Enter**.
* Paste your **Chat ID** and save.


3. **Start the Bot**:
Search for [@NASLinuxVbot](https://www.google.com/search?q=https://t.me/NASLinuxVbot) on Telegram and press **Start**.
4. **Verify Connection**:
Restart the **MSG** and **DUFS** services from the main menu. If successful, you will receive a message saying **"Checking state"** from the bot.

---

## 🛠 Features

| Feature | Description |
| --- | --- |
| **Terminal UI** | A beautiful interface using the `Rich` library for system control. |
| **Web Menu** | Access your NAS management via browser at `http://[YOUR_IP]:8000/menu`. |
| **DUFS (FTP)** | High-performance file server running on port `5000`. |
| **Docker MSG** | Containerized messenger service for secure status reporting. |
| **Disk Utility** | Real-time monitoring of disk usage and partition layouts. |
| **System Info** | Live tracking of CPU temperature, Uptime, and RAM usage. |

---

## 🖥 Screenshots (Coming Soon)

*(You can add your images here later!)*

## 🛡 Security Note

Ensure you do not share your `settings.csv` or `config.json` files publicly, as they contain your private Telegram configuration.

---

**Developed with ❤️ by [Edgit13**](https://www.google.com/search?q=https://github.com/Edgit13)

```
