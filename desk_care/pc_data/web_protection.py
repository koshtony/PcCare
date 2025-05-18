import os
import sys
import subprocess
import socket
import ctypes 

from urllib.parse import urlparse
from duckduckgo_search import DDGS


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
            
            
                    
    
    
