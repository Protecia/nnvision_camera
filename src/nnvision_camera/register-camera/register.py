#!/usr/bin/env python3
import os
import re
import hashlib
from pathlib import Path
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from getpass import getpass
from requests.auth import HTTPBasicAuth
import time

# ========= Configuration =========
DRF_ENDPOINT = os.environ.get("DRF_ENDPOINT", "http://192.168.1.38:8000/api/devices/register/")
BASIC_USER = os.environ.get("BASIC_USER")
BASIC_PASS = os.environ.get("BASIC_PASS")
# =================================

def get_rpi_serial() -> str:
    """Récupère le numéro de série du Raspberry Pi."""
    p = Path("/proc/device-tree/serial-number")
    if p.exists():
        s = p.read_text(errors="ignore").strip().strip("\x00").lower()
        if s and re.fullmatch(r"[0-9a-f]+", s):
            return s
    for line in Path("/proc/cpuinfo").read_text(errors="ignore").splitlines():
        if line.lower().startswith("serial"):
            _, val = line.split(":", 1)
            return val.strip().lower()
    raise RuntimeError("Impossible de lire le numéro de série du Raspberry Pi.")

def _read_first_existing(paths):
    for p in paths:
        fp = Path(p)
        if fp.exists():
            return fp.read_text(errors="ignore").strip()
    return None

def get_sd_identifier() -> str:
    """Récupère l'identifiant de la carte SD (CID ou serial)."""
    for dev in ("mmcblk0", "mmcblk1"):
        cid = _read_first_existing([f"/sys/block/{dev}/device/cid", f"/sys/block/{dev}/device/serial"])
        if cid:
            return cid.replace(" ", "").replace("\x00", "").strip()
    raise RuntimeError("Impossible de lire l'identifiant de la carte SD.")

def derive_password(rpi_serial: str, sd_id: str) -> str:
    """Construit le mot de passe comme hash SHA256 du couple RPi+SD."""
    msg = f"{rpi_serial}:{sd_id}".encode("utf-8")
    return hashlib.sha256(msg).hexdigest()

def make_session_with_retries():
    retry = Retry(total=3, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504))
    adapter = HTTPAdapter(max_retries=retry)
    s = requests.Session()
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s

def main():
    # --- Auth Basic ---
    username = BASIC_USER or input("Identifiant (Basic Auth): ").strip()
    password_prompt = BASIC_PASS or getpass("Mot de passe (Basic Auth): ")
    auth = HTTPBasicAuth(username, password_prompt)

    # --- Empreintes device ---
    rpi_serial = get_rpi_serial()
    print(f"The serial number for the rpi is {rpi_serial}")
    sd_id = get_sd_identifier()
    print(f"The serial number for the SD card is {sd_id}")
    derived_pwd = derive_password(rpi_serial, sd_id)
    print(f"The derived password is {derived_pwd}")
    time.sleep(1)  # pour que l'utilisateur ait le temps de lire

    # --- Payload minimal ---
    payload = {"password": derived_pwd}

    # --- POST ---
    session = make_session_with_retries()
    resp = session.post(DRF_ENDPOINT, json=payload, auth=auth, timeout=5)

    print("Status:", resp.status_code)
    try:
        print("Réponse JSON:", resp.json())
    except Exception:
        print("Réponse brute:", resp.text)

if __name__ == "__main__":
    main()
