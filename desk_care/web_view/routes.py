from flask import Flask,render_template 
from pc_data.pc_info import get_cpu_battery,get_cpu_temperature,\
    get_cpu_performance,get_upload_download_speed,calculate_usage
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
    
    temp = get_cpu_temperature()
    
    return {"temp":temp}

@app.route('/get_cpu_performance')
def get_cpu_perf_view():

    times,freq= get_cpu_performance()
    
    print(times)
    
    return {"times":times,"freq":freq}


@app.route('/get_chart_data')
def get_chart_data():
    
    times,freq= get_cpu_performance()
    
    data = {
        
        "current":freq.current,
        "min":freq.min,
        "max":freq.max,
        
     
    }
    
    return data

@app.route('/get_download_upload_speed')
def get_download_upload_speed_view():
    
    download_speed,upload_speed = get_upload_download_speed()
    
    return {"download_speed":download_speed,"upload_speed":upload_speed}