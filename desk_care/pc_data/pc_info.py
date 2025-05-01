import psutil
import subprocess
import os
import wmi
import time
import pythoncom
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
        
        if len(output) >= 2:
           
            temp_kelvin = int(output[2])
            temp_celsius = temp_kelvin - 273.15
            return round(temp_celsius, 2)
        else:
            return "Temperature data not available."
    except Exception as e:
        return f"Error: {e}"
    
    
def get_cpu_performance():
    
    return psutil.cpu_times(),psutil.cpu_freq()


    
    