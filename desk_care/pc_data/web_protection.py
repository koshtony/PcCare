import os
import sys
import subprocess
import socket
import ctypes 

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
    
   
  
    try:
        for website in websites:
            
            ip_address = socket.gethostbyname(website)
            
            rule_name =  f"Block {ip_address}"
            cmd =   f'netsh advfirewall firewall add rule name="{rule_name}" dir=out action=block remoteip={ip_address} enable=yes'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            resp = result.stdout or result.stderr
    except Exception as e:
        resp = f"Error: {e}"
    return resp
            
            
                    
    
    
