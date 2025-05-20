import os
import subprocess
import urllib.request
import threading
import pyshark
import asyncio
from scapy.all import sniff, DNSQR
import threading

NPCAP_URL = "https://nmap.org/npcap/dist/npcap-1.78.exe"
INSTALLER_NAME = "npcap.exe"
INSTALLER_PATH = os.path.join(os.getcwd(), INSTALLER_NAME)
visited_domains = set()
_capture_thread = None

def is_npcap_installed():
    try:
        result = subprocess.run(["tshark", "-D"], capture_output=True, text=True, timeout=5)
        return "Npcap" in result.stdout or len(result.stdout.strip()) > 0
    except Exception:
        return False
    


def download_npcap():
    print("[*] Downloading Npcap...")
    urllib.request.urlretrieve(NPCAP_URL, INSTALLER_NAME)
    print("[+] Npcap downloaded.")
    
def run_npcap_installer(path):
    if os.path.exists(path):
        print("[*] Launching Npcap installer...")
        os.startfile(path)
    else:
        print("[!] Installer not found at:", path)
    
def prompt_user_to_install_npcap():
    print("\n[!] Npcap is required but not installed.")
    print(f"[i] Installer downloaded at: {INSTALLER_PATH}")
    run_npcap_installer(INSTALLER_PATH)
    input("[*] Please run the installer manually. Press Enter once you've finished...\n")

def install_npcap_silent():
    print("[*] Installing Npcap silently...")
    subprocess.run([
        INSTALLER_NAME,
        "/S",
        "/winpcap_mode=yes",
        "/loopback_support=yes",
    ], check=True)
    print("[+] Npcap installed.")

def ensure_npcap():
    if os.path.exists(INSTALLER_PATH):
        return  # Skip check if previously marked installed

    if not is_npcap_installed():
        if not os.path.exists(INSTALLER_PATH):
            download_npcap()
        run_npcap_installer(INSTALLER_PATH)
        input("[*] After installing Npcap, press Enter to continue...\n")

        # After user confirms
        if is_npcap_installed():
            with open(INSTALLER_PATH, "w") as f:
                f.write("Npcap installed")
            print("[+] Npcap installation confirmed.")
        else:
            print("[!] Npcap still not detected. Please try again.")

def _sniff(interface="Wi-Fi"):
    try:
        print(f"[*] Starting packet capture on interface: {interface}")
        
        def packet_handler(packet):
            if packet.haslayer(DNSQR):
                domain = packet[DNSQR].qname.decode().rstrip('.')
                if domain and domain not in visited_domains:
                    visited_domains.add(domain)
                    print(f"[+] Domain visited: {domain}")
        
        sniff(filter="udp port 53", iface=interface, prn=packet_handler, store=0)
    
    except Exception as e:
        print(f"[!] Capture error: {e}")

def start_sniffer():
    global _capture_thread
    _capture_thread = threading.Thread(target=_sniff, daemon=True)
    _capture_thread.start()

def is_sniffer_running():
    return _capture_thread is not None and _capture_thread.is_alive()
