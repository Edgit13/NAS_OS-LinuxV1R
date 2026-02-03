#!/usr/bin/env python3
import os
import json
import subprocess
import time
import sys
import select
import csv
import socket
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from translations import get_text

console = Console()
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

def load_token_from_csv():
    """Reads secret token from settings.csv"""
    csv_path = os.path.join(PROJECT_PATH, 'settings.csv')
    try:
        if os.path.exists(csv_path):
            with open(csv_path, mode='r') as f:
                content = f.read().strip()
                return content if content else ""
    except: pass
    return ""

def load_config():
    config_file = os.path.join(PROJECT_PATH, 'config.json')
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {
            "os_name": "NAS_OS", 
            "theme_color": "cyan", 
            "language": "uk",
            "tg_token": "",
            "tg_chat_id": ""
        }
    
    if not config.get("tg_token"):
        csv_token = load_token_from_csv()
        if csv_token:
            config["tg_token"] = csv_token
            save_config(config)
            
    return config

def save_config(config):
    with open(os.path.join(PROJECT_PATH, 'config.json'), 'w') as f:
        json.dump(config, f, indent=2)

def get_ip():
    """Gets real local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return subprocess.check_output(["hostname", "-I"]).decode().strip().split()[0]
        except:
            return "127.0.0.1"

def get_status():
    status_dufs = "[bold red]OFF[/bold red]"
    status_web  = "[bold red]OFF[/bold red]"
    status_msg  = "[bold red]OFF[/bold red]"

    try:
        subprocess.check_output(["pgrep", "-f", "dufs"], stderr=subprocess.DEVNULL)
        status_dufs = "[bold green]ON[/bold green]"
    except: pass

    try:
        subprocess.check_output(["pgrep", "-f", "NAS_OS-LinuxV--MENU -web.py"], stderr=subprocess.DEVNULL)
        status_web = "[bold green]ON[/bold green]"
    except: pass

    try:
        out = subprocess.check_output(["docker", "inspect", "-f", "{{.State.Running}}", "debian-msg"], stderr=subprocess.DEVNULL)
        if out.decode().strip() == "true":
            status_msg = "[bold green]ON[/bold green]"
    except: pass

    return f"DUFS: {status_dufs} | WEB: {status_web} | MSG: {status_msg}"

def toggle_dufs():
    subprocess.run([os.path.join(PROJECT_PATH, "NAS_OS--ftpS.sh")])
    time.sleep(1.5)

def toggle_web():
    conf = load_config()
    lang = conf.get('language', 'uk')
    try:
        subprocess.check_output(["pgrep", "-f", "NAS_OS-LinuxV--MENU -web.py"], stderr=subprocess.DEVNULL)
        subprocess.run(["pkill", "-f", "NAS_OS-LinuxV--MENU -web.py"])
        console.print(f"\n[bold red]{get_text('web_stopped', lang)}[/bold red]")
    except subprocess.CalledProcessError:
        subprocess.Popen(
            ["python3", os.path.join(PROJECT_PATH, "NAS_OS-LinuxV--MENU -web.py")],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True
        )
        console.print(f"\n[bold green]{get_text('web_started', lang)}[/bold green]")
    time.sleep(1.5)

def toggle_messenger():
    conf = load_config()
    lang = conf.get('language', 'uk')

    def send_state_check():
        """Wait 1s and send the TCP check command"""
        time.sleep(1)
        try:
            # shell=True is used to support the pipe (|)
            subprocess.run("echo 'Checking state' | nc -N localhost 12345", shell=True, check=False)
        except Exception as e:
            console.print(f"[dim red]State check failed: {e}[/dim red]")

    try:
        out = subprocess.check_output(["docker", "inspect", "-f", "{{.State.Running}}", "debian-msg"], stderr=subprocess.DEVNULL)
        if out.decode().strip() == "true":
            subprocess.run(["docker", "stop", "debian-msg"], stdout=subprocess.DEVNULL)
            subprocess.run(["pkill", "-f", "log_monitor.py"])
            console.print(f"\n[bold red]MSG & Monitor Stopped[/bold red]")
        else:
            subprocess.run(["docker", "start", "debian-msg"], stdout=subprocess.DEVNULL)
            subprocess.Popen(["python3", os.path.join(PROJECT_PATH, "log_monitor.py")], 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            console.print(f"\n[bold green]MSG & Monitor Started[/bold green]")
            send_state_check()
    except subprocess.CalledProcessError:
        console.print("\n[yellow]Container not found. Starting fresh...[/yellow]")
        subprocess.run([
            "docker", "run", "-d", "--name", "debian-msg", 
            "-p", "12345:12345", 
            "-v", f"{PROJECT_PATH}/config.json:/app/config.json:ro",
            "nas-messenger"
        ])
        subprocess.Popen(["python3", os.path.join(PROJECT_PATH, "log_monitor.py")], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        send_state_check()
    
    time.sleep(1.5)

def show_disk():
    conf = load_config()
    lang = conf.get('language', 'uk')
    os.system('clear')
    console.print(f"[bold cyan]═══ {get_text('disk_info_title', lang)} ═══[/bold cyan]\n")
    os.system('lsblk -o NAME,SIZE,TYPE,MOUNTPOINT')
    console.print(f"\n[bold cyan]═══ {get_text('disk_usage', lang)} ═══[/bold cyan]\n")
    os.system('df -h')
    input(f"\n{get_text('press_enter', lang)}")

def show_sys_info():
    conf = load_config()
    lang = conf.get('language', 'uk')
    os.system('clear')
    console.print(f"[bold cyan]═══ {get_text('sys_info_title', lang)} ═══[/bold cyan]\n")
    ip = get_ip()
    console.print(f"[green]{get_text('ip_address', lang)}[/green] {ip}")
    try:
        up = subprocess.check_output(["uptime", "-p"]).decode().strip()
        console.print(f"[green]{get_text('uptime', lang)}[/green] {up}")
    except: pass
    
    console.print(f"\n[bold cyan]═══ {get_text('running_services', lang)} ═══[/bold cyan]\n")
    for service, cmd, port in [
        (get_text('dufs_server', lang), "dufs", "5000"),
        (get_text('web_menu', lang), "NAS_OS-LinuxV--MENU -web.py", "8000/menu")
    ]:
        try:
            subprocess.check_output(["pgrep", "-f", cmd], stderr=subprocess.DEVNULL)
            console.print(f"[bold green]✓ {service}[/bold green] [cyan]→ http://{ip}:{port}[/cyan]")
        except:
            console.print(f"[bold red]✗ {service}[/bold red]")

    try:
        subprocess.check_output(["docker", "inspect", "debian-msg"], stderr=subprocess.DEVNULL)
        console.print(f"[bold green]✓ Debian Messenger (Docker)[/bold green] [cyan]→ Port 12345[/cyan]")
    except:
        console.print(f"[bold red]✗ Debian Messenger[/bold red]")

    console.print(f"\n[bold cyan]═══ {get_text('memory', lang)} ═══[/bold cyan]\n")
    os.system('free -h')
    try:
        t = int(open("/sys/class/thermal/thermal_zone0/temp").read().strip()) / 1000
        console.print(f"\n[green]{get_text('cpu_temp', lang)}[/green] {t:.1f}°C")
    except: pass
    input(f"\n[yellow]{get_text('press_enter_return', lang)}[/yellow]")

def show_settings():
    while True:
        conf = load_config()
        lang = conf.get('language', 'uk')
        os.system('clear')
        console.print(f"[bold cyan]═══ {get_text('settings_title', lang)} ═══[/bold cyan]\n")
        console.print(f"1. {get_text('select_language', lang)} (Current: {lang})")
        console.print(f"2. {get_text('tg_id_label', lang)} (ID: {conf.get('tg_chat_id', '---')})")
        console.print(f"B. {get_text('press_enter_return', lang)}")
        
        choice = input(f"\n{conf['os_name']} > ").strip().upper()
        if choice == '1':
            console.print("1. UA | 2. EN")
            l_choice = input(">> ")
            conf['language'] = 'uk' if l_choice == '1' else 'en'
            save_config(conf)
        elif choice == '2':
            new_id = input("Введіть ваш Chat ID: ").strip()
            if new_id:
                conf['tg_chat_id'] = new_id
                save_config(conf)
                console.print("[green]Chat ID збережено![/green]")
                time.sleep(1)
        elif choice == 'B' or choice == '':
            break

def print_menu():
    conf = load_config()
    lang = conf.get('language', 'uk')
    os.system('clear')
    logo = "    █▄ █ ▄▀█ █▀    █▀█ █▀\n    █ ▀█ █▀█ ▄█    █▄█ ▄█"
    
    status_line = get_status()
    header_content = f"{logo}\n\n[bold]{conf['os_name']}[/bold]\n{get_text('status', lang)}: {status_line}"
    header = Panel(Align.center(header_content), border_style=conf.get('theme_color','cyan'), padding=(1, 1))

    t = Table(show_header=False, box=None, expand=True)
    t.add_column("ID", style="bold yellow", width=4)
    t.add_column("Action")
    t.add_row("1", get_text('toggle_dufs', lang))
    t.add_row("2", get_text('toggle_web', lang))
    t.add_row("3", "Toggle Messenger & Monitor")
    t.add_row("4", get_text('disk_info', lang))
    t.add_row("5", get_text('system_info', lang))
    t.add_row("6", get_text('settings', lang))
    t.add_row("Q", get_text('exit', lang))

    console.print(Align.center(Group(header, Panel(t, title=get_text('main_menu', lang), border_style="dim"))))
    console.print(f"\n[bold yellow]{conf['os_name']} > [/bold yellow]", end="")

def run_intro():
    conf = load_config()
    lang = conf.get('language', 'uk')
    os.system('clear')
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%")) as progress:
        t1 = progress.add_task(f"[cyan]{get_text('booting', lang)}", total=100)
        while not progress.finished:
            time.sleep(0.01)
            progress.update(t1, advance=3)

if __name__ == "__main__":
    run_intro()
    while True:
        try:
            print_menu()
            r, _, _ = select.select([sys.stdin], [], [], 5)
            if r:
                choice = sys.stdin.readline().strip().upper()
                if   choice == '1': toggle_dufs()
                elif choice == '2': toggle_web()
                elif choice == '3': toggle_messenger()
                elif choice == '4': show_disk()
                elif choice == '5': show_sys_info()
                elif choice == '6': show_settings()
                elif choice == 'Q':
                    console.print(f"\n[bold red]{get_text('goodbye', load_config().get('language','uk'))}[/bold red]")
                    sys.exit()
        except KeyboardInterrupt: sys.exit()
