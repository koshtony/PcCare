from flask import Flask,render_template 
from pc_data.pc_info import get_cpu_battery,get_cpu_temperature,\
    get_cpu_performance,get_upload_download_speed,calculate_usage
from pc_data.web_protection import block_sites_using_host_file,block_sites_using_firewall,set_to_admin
from flask import jsonify

from web_view import app
@app.route('/')
def home_page():
    """
    Render the home page of the web interface.

    Returns:
        The rendered template for the home page.
    """
    cpu_temperature = get_cpu_temperature()
    cpu_performance = get_cpu_performance()
    
    temp = get_cpu_temperature()
    #battery = get_cpu_battery()
    times,freq= get_cpu_performance()
    
    times = {
        
        "user":times.user//60,
        "system":times.system,
        "idle":times.idle,
     
    }
    
    freq = {
        
        "current":freq.current,
        "min":freq.min,
        "max":freq.max,
    }
    
    cpu,memory,disk = calculate_usage()
    
    
   
    return render_template(
        'index.html',
       times=times,freq=freq,temp=temp,
       cpu=cpu,memory=memory,disk=disk
      
        
    )


@app.route('/get_temperature')
def get_temp_view(): 
    

    """
    Retrieve the current CPU temperature.

    Returns:
        dict: A dictionary containing the current CPU temperature with
        the key 'temp'.
    """


    temp = get_cpu_temperature()
    
    return {"temp":temp}

@app.route('/get_cpu_performance')
def get_cpu_perf_view():


    """
    Retrieve the current CPU performance metrics.

    Returns:
        dict: A dictionary containing the current CPU performance metrics
        with the keys 'times' and 'freq'. The 'times' key contains a
        dictionary of CPU times with the keys 'user', 'system', and 'idle',
        while the 'freq' key contains a dictionary of CPU frequency metrics
        with the keys 'current', 'min', and 'max'.
    """


    times,freq= get_cpu_performance()
    
    print(times)
    
    return {"times":times,"freq":freq}


@app.route('/get_chart_data')
def get_chart_data():

    """
    Retrieve the current CPU frequency data for the chart.

    Returns:
        dict: A dictionary containing the current CPU frequency data
        with the keys 'current', 'min', and 'max'.
    """


    times,freq= get_cpu_performance()
    
    data = {
        
        "current":freq.current,
        "min":freq.min,
        "max":freq.max,
        
     
    }
    
    return data

@app.route('/get_download_upload_speed')
def get_download_upload_speed_view():
    

    """
    Retrieve the current download and upload speeds.

    Returns:
        dict: A dictionary containing the current download and upload speeds
        with the keys 'download_speed' and 'upload_speed'.
    """

    download_speed,upload_speed = get_upload_download_speed()
    
    return {"download_speed":download_speed,"upload_speed":upload_speed}


@app.route('/block_sites')
def block_sites_view():
    
    set_to_admin()
    
    
    sites = ["www.facebook.com", "facebook.com"]
    print("=========Host File Method===========")
    try:
    
        resp = block_sites_using_host_file(sites)
        print(resp)
        
    except Exception as e: 
        
        resp = f"Error: {e}"
        print(resp)
        
    print("=========Attempting Firewall Method===========")
    
    try:
    
        resp = block_sites_using_firewall(sites)
        print(resp)
        
    except Exception as e: 
        
        resp = f"Error: {e}"
        
        print(resp)
    
    return render_template('web_protection.html')
    
    