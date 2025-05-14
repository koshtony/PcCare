import psutil
import subprocess
import os
import wmi
import time
import pythoncom
#import speedtest as spt 
def get_cpu_battery():
    
    
    battery = psutil.sensors_battery()
    return battery


def get_cpu_temperature():
    
    try:
        output = subprocess.check_output(
            ["wmic", "path", "Win32_PerfFormattedData_Counters_ThermalZoneInformation", "get", "Temperature"],
            shell=True
        )
        output = output.decode().strip().split()
        
        print(len(output))
        
        if len(output) >= 2:
           
            temp_kelvin = int(output[1])
            temp_celsius = temp_kelvin - 273.15
            return round(temp_celsius, 2)
        
       
            
        else:
            return "Temperature data not available."
    except Exception as e:
        return f"Error: {e}"
    
    
def get_cpu_performance():
    
    return psutil.cpu_times(),psutil.cpu_freq()

'''

def get_upload_download_speed(): 
    
    st = spt.Speedtest()

    st.get_best_server()

    download_speed = st.download()

    upload_speed = st.upload()
    
    
    return f"{download_speed / 1_000_000:.2f} Mbps",f"{upload_speed / 1_000_000:.2f} Mbps"

'''
def calculate_usage():
    
    cpu,memory,disk = psutil.cpu_percent(interval=1),psutil.virtual_memory().percent,psutil.disk_usage('/').percent	

    return cpu,memory,disk
    
    