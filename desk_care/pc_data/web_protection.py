import os
import sys
import subprocess
import socket
import ctypes 
import requests
from bs4 import BeautifulSoup
from scapy.all import sniff, DNSQR
from urllib.parse import urlparse
from duckduckgo_search import DDGS
import pyshark
import asyncio
import time
import re


def set_to_admin(): 
    
     ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1
        )
def block_sites_using_host_file(domains):
    
    
    
    hosts_path = "/etc/hosts" if os.name != "nt" else r"C:\Windows\System32\drivers\etc\hosts"
    redirect_ip = "127.0.0.1"
    
    try: 
        
        with open(hosts_path,"r+") as file:
            content = file.read()
            for website in domains:
                if website not in content:
                    entry = f"{redirect_ip} {website}\n"
                    if entry not in content:
                        file.write(entry)
            resp = f"Website Blocked successfully"
    except Exception as e:
        resp = f"Error: {e}"
    return resp



def block_sites_using_firewall(websites):
    

    """
    Blocks the specified websites using the system's firewall.

    This function takes a list of website URLs, resolves their IP addresses,
    and adds firewall rules to block outgoing traffic to these IPs. It uses
    the Windows 'netsh' command to add firewall rules.

    Args:
        websites (list): A list of website URLs to block.

    Returns:
        str: The standard output or error message from the firewall command execution.
    """

    try:
        
        resp = ""
        for website in websites:
            
            print(website)
            
            ip_address = socket.gethostbyname(website)
            
            rule_name =  f"Block {ip_address}"
            cmd =   f'netsh advfirewall firewall add rule name="{rule_name}" dir=out action=block remoteip={ip_address} enable=yes'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            resp += result.stdout or result.stderr
    except Exception as e:
        resp = f"Error: {e}"
    return resp

def unblock_site_firewall_method(sites):
    
    try:
        
        resp = ""
        for site in sites:
            ip_address = socket.gethostbyname(site)
            
            rule_name = f"Block {ip_address}"
            
            cmd = f'netsh advfirewall firewall delete rule name="{rule_name}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            resp +=  result.stdout or result.stderr
            
    except Exception as err:
        
        resp = f"Error: {err}"
        
    return resp

def unblock_site_host_method(domains): 
    
    HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
    if not os.path.exists(HOSTS_PATH):
        print("❌ Hosts file not found.")
        return

    with open(HOSTS_PATH, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        if not any(domain in line for domain in domains):
            new_lines.append(line)

    with open(HOSTS_PATH, 'w') as file:
        file.writelines(new_lines)

    return "✅ Unblocked sites:", ", ".join(domains)

def unblock_individual_domain_host_method(domain): 
    
    hosts_path = "/etc/hosts" if os.name != "nt" else r"C:\Windows\System32\drivers\etc\hosts"
    
    try:
        with open(hosts_path, 'r') as file:
            lines = file.readlines()

        new_lines = []
        found = False
        for line in lines:
            if domain in line and ("127.0.0.1" in line or "0.0.0.0" in line):
                found = True
                # skip this line (unblock)
                continue
            new_lines.append(line)

        if found:
            with open(hosts_path, 'w') as file:
                file.writelines(new_lines)
            return f"✅ Unblocked: {domain}"
        else:
            return f"ℹ️ Domain not blocked: {domain}"

    except PermissionError:
        return "❌ Permission denied. Please run this script as administrator or with sudo."
    except Exception as e:
        return f"❌ Error: {e}"


def list_blocked_sites(): 
    
    HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
    BLOCKED_IPS = ["127.0.0.1", "0.0.0.0"]
    
    blocked = []
    if not os.path.exists(HOSTS_PATH):
        return blocked

    with open(HOSTS_PATH, 'r') as file:
        for line in file:
            if line.strip().startswith("#") or not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) >= 2 and parts[0] in BLOCKED_IPS:
                blocked.append(parts[1])
    return blocked


def get_site_text_summary(domain):
    
    
    if not domain.startswith("http"):
        domain = "http://" + domain  # fallback to HTTP

    try:
        response = requests.get(domain, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove scripts and styles
        for tag in soup(['script', 'style', 'noscript']):
            tag.decompose()

        # Extract visible text
        text = soup.get_text(separator='\n')
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        if lines:
            return lines[0]  # first non-empty line
        else:
            return "No visible content found."

    except Exception as e:
        return f"Error fetching domain: {e}"
    
    
def get_domain_info(sites):
    
    site_info = []
    
    for site in sites:
        
        info = {
            
            "name":site.split(".")[0] if len(site.split("."))==2 else site.split(".")[1],
            "domain":site,
            "ip adrress":socket.gethostbyname(site),
            "content":get_site_text_summary(site)
        }
        
        site_info.append(info)
        
    
        
    return site_info



pktmon_txt = "PktMon.txt"


def remove_old_files():
    for file in ["PktMon.etl", "PktMon.txt"]:
        if os.path.exists(file):
            os.remove(file)
            print(f"Removed old file: {file}")
            
            
def run_pktmon_capture(duration=30):
    
    try:
        remove_old_files()
        subprocess.run("pktmon start --etw", shell=True, check=True)
        print("Pktmon started.")
        
        time.sleep(duration)
        
        subprocess.run("pktmon stop", shell=True, check=True)
        print("Pktmon stopped.")
        
        subprocess.run("pktmon format PktMon.etl -o PktMon.txt", shell=True, check=True)
        print("Pktmon formatted.")
    except subprocess.CalledProcessError as e:
        print(f"Error during pktmon operation: {e}")
        

def extract_domains_from_pktmon():
   
    if not os.path.exists(pktmon_txt):
       
        return []

    query_patterns = [
    re.compile(r"Query Name\s*:\s*(\S+)", re.IGNORECASE),
    re.compile(r"DNS Query\s*:\s*(\S+)", re.IGNORECASE),
    ]

    domains = set()

    with open(pktmon_txt, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            print(line.strip())
            for pattern in query_patterns:
                match = pattern.search(line)
                if match:
                    domain = match.group(1).lower()
                    domains.add(domain)
    return sorted(domains)

    
    
    
        
        

    
    



def get_site_domains_from_keywords(keyword, max_results):
    
    results = DDGS().text(keyword, max_results=max_results)
    domains = set()

    for r in results:
        url = r.get("href")
        if url:
            parsed = urlparse(url)
            netloc = parsed.netloc
            # Normalize: add www if missing
            if netloc and not netloc.startswith("www."):
                netloc = "www." + netloc
            domains.add(netloc)

    return sorted(domains)
            
            
                    
    
    
