#!/usr/bin/env python3
from flask import Flask, render_template_string, redirect, url_for, request, session
import subprocess
import os
import json
from functools import wraps
from style import STYLE_CSS
from translations import get_text

app = Flask(__name__)
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

# ─── users.json ───────────────────────────────
def load_users():
    path = os.path.join(PROJECT_PATH, 'users.json')
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        default = {
            "users": [{"username": "admin", "password": "admin123", "role": "admin"}],
            "session_secret": "change-this-secret-key"
        }
        with open(path, 'w') as f:
            json.dump(default, f, indent=2)
        return default

def load_config():
    """Load config including language"""
    path = os.path.join(PROJECT_PATH, 'config.json')
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"os_name": "NAS_OS", "theme_color": "cyan", "language": "uk"}

users_data = load_users()
app.secret_key = users_data.get('session_secret', 'default-secret')

# ─── auth ─────────────────────────────────────
def login_required(f):
    @wraps(f)
    def wrapper(*a, **kw):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*a, **kw)
    return wrapper

def verify(username, password):
    return any(
        u['username'] == username and u['password'] == password
        for u in users_data['users']
    )

# ─── helpers ──────────────────────────────────
def dufs_running():
    try:
        subprocess.check_output(["pgrep", "-f", "dufs"], stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def terminal_menu_running():
    try:
        subprocess.check_output(["pgrep", "-f", "NAS_OS-LinuxV--MENU.py"], stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def get_disk_usage():
    try:
        st = os.statvfs(PROJECT_PATH)
        free  = (st.f_bavail * st.f_frsize) / (1024**3)
        total = (st.f_blocks * st.f_frsize) / (1024**3)
        used  = total - free
        pct   = int((used / total) * 100)

        df_out = subprocess.check_output(['df', PROJECT_PATH]).decode().splitlines()[1]
        device = df_out.split()[0].split('/')[-1]

        return {"total": f"{total:.1f}", "free": f"{free:.1f}", "pct": pct, "device": device}
    except:
        return {"total": "0", "free": "0", "pct": 0, "device": "N/A"}

def get_ip():
    try:
        return subprocess.check_output(["hostname", "-I"]).decode().strip().split()[0]
    except:
        return "N/A"

# ─── routes ───────────────────────────────────
@app.route('/')
def index():
    return redirect(url_for('menu'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    conf = load_config()
    lang = conf.get('language', 'uk')
    
    error = None
    if request.method == 'POST':
        if verify(request.form.get('username',''), request.form.get('password','')):
            session['logged_in'] = True
            session['username']  = request.form['username']
            return redirect(url_for('menu'))
        error = "Invalid username or password" if lang == "en" else "Невірний логін або пароль"

    login_text = "Login to continue" if lang == "en" else "Увійдіть для продовження"
    username_text = "Username" if lang == "en" else "Логін"
    password_text = "Password" if lang == "en" else "Пароль"
    login_btn = "LOGIN" if lang == "en" else "УВІЙТИ"
    
    return render_template_string(f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NAS OS – Login</title>
    {STYLE_CSS}
</head>
<body>
<div class="login-container">
    <header>
        <h1>🔐 NAS OS</h1>
        <p style="color:var(--gray);font-size:14px;">{login_text}</p>
    </header>
    <div class="login-card">
        {'<div class="error-msg">'+error+'</div>' if error else ''}
        <form method="POST">
            <div class="form-group">
                <label>{username_text}</label>
                <input type="text" name="username" required autofocus>
            </div>
            <div class="form-group">
                <label>{password_text}</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit" class="btn-login">{login_btn}</button>
        </form>
    </div>
</div>
</body>
</html>''')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/menu')
@login_required
def menu():
    conf = load_config()
    lang = conf.get('language', 'uk')
    
    dufs  = dufs_running()
    term  = terminal_menu_running()
    disk  = get_disk_usage()
    ip    = get_ip()
    user  = session.get('username', '')

    def dot(on):
        return 'online' if on else 'offline'
    
    # Translations
    storage = "Storage" if lang == "en" else "Сховище"
    free_text = "Free" if lang == "en" else "Вільно"
    of_text = "of" if lang == "en" else "з"
    used_text = "used" if lang == "en" else "використано"
    port = "Port" if lang == "en" else "Порт"
    running = "Running" if lang == "en" else "Запущено"
    stopped = "Stopped" if lang == "en" else "Зупинено"
    logout_text = "LOGOUT" if lang == "en" else "ВИЙТИ"
    reboot_text = "REBOOT SYSTEM" if lang == "en" else "ПЕРЕЗАВАНТАЖИТИ"
    reboot_confirm = "Reboot?" if lang == "en" else "Перезавантажити?"
    auto_refresh = "auto-refresh 5s" if lang == "en" else "авто-оновлення 5с"
    backup_title = "Backup" if lang == "en" else "Бекап"
    backup_btn_text = "RUN BACKUP" if lang == "en" else "СТВОРИТИ БЕКАП"

    return render_template_string(f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="5">
    <title>NAS OS Control</title>
    {STYLE_CSS}
</head>
<body>
<div class="dashboard">
    <header>
        <h1>📡 NAS OS</h1>
        <p style="color:var(--gray);font-size:13px;">{user} · {ip}</p>
    </header>

    <div class="card">
        <h3>💾 {storage} <span style="font-size:12px;color:var(--gray);">{disk['device']}</span></h3>
        <div class="disk-meta">{free_text} {disk['free']} GB {of_text} {disk['total']} GB</div>
        <div class="progress-bar"><div class="progress-fill" style="width:{disk['pct']}%"></div></div>
        <div style="text-align:right;font-size:11px;margin-top:5px;color:var(--gray);">{disk['pct']}% {used_text}</div>
    </div>

    <div class="card">
        <h3>🌐 {get_text('dufs_server', lang)} <span class="status-dot {dot(dufs)}"></span></h3>
        <div class="btn-group">
            <a href="/action/dufs/start" class="btn btn-on">START</a>
            <a href="/action/dufs/stop"  class="btn btn-off">STOP</a>
        </div>
        <div style="margin-top:10px;font-size:12px;color:var(--gray);">
            {port} 5000 · {running if dufs else stopped}
        </div>
    </div>

    <div class="card">
        <h3>💻 {get_text('terminal_menu', lang)} <span class="status-dot {dot(term)}"></span></h3>
        <div class="btn-group">
            <a href="/action/terminal/start" class="btn btn-on">START</a>
            <a href="/action/terminal/stop"  class="btn btn-off">STOP</a>
        </div>
        <div style="margin-top:10px;font-size:12px;color:var(--gray);">
            {running if term else stopped}
        </div>
    </div>

    <div class="card">
        <h3>📂 {backup_title}</h3>
        <div class="btn-group">
            <a href="/action/backup" class="btn btn-on" style="width:100%; text-align:center; background-color:var(--cyan);">{backup_btn_text}</a>
        </div>
        <div style="margin-top:10px;font-size:11px;color:var(--gray);">
            Target: shared_files/ (tar.gz)
        </div>
    </div>

    <div style="text-align:center;margin-top:24px;display:flex;gap:24px;justify-content:center;">
        <a href="/logout" class="logout-btn">{logout_text}</a>
        <a href="/reboot" style="color:var(--red);text-decoration:none;font-size:12px;font-weight:bold;"
           onclick="return confirm('{reboot_confirm}')">{reboot_text}</a>
    </div>
    <div style="text-align:center;margin-top:12px;font-size:11px;color:var(--gray);">{auto_refresh}</div>
</div>
</body>
</html>''')

# ─── actions ──────────────────────────────────
@app.route('/action/<svc>/<state>')
@login_required
def action(svc, state):
    if svc == 'dufs':
        if state == 'start':
            subprocess.Popen([os.path.join(PROJECT_PATH, "NAS_OS--ftpS.sh")])
        else:
            subprocess.run(["pkill", "-f", "dufs"])

    elif svc == 'terminal':
        if state == 'start':
            subprocess.Popen(
                ["python3", os.path.join(PROJECT_PATH, "NAS_OS-LinuxV--MENU.py")],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        else:
            subprocess.run(["pkill", "-f", "NAS_OS-LinuxV--MENU.py"])

    return redirect(url_for('menu'))

@app.route('/action/backup')
@login_required
def backup():
    # Запуск скрипта бекапу
    subprocess.Popen(["bash", os.path.join(PROJECT_PATH, "backup.sh")])
    return redirect(url_for('menu'))

@app.route('/reboot')
@login_required
def reboot():
    subprocess.Popen(["sudo", "reboot"])
    return "Rebooting..."

# ─── main ─────────────────────────────────────
if __name__ == '__main__':
    print("NAS OS Web → http://0.0.0.0:8000/menu")
    app.run(host='0.0.0.0', port=8000, debug=False)
