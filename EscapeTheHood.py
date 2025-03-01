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
2. TAILS OS: Snag latest Tails ISO (tails.net), flash it with Rufus. Boot USB (F12), ghost