from flask import Flask,render_template,request
from pc_data.pc_info import get_cpu_battery,get_cpu_temperature,\
    get_cpu_performance,calculate_usage
from pc_data.web_protection import block_sites_using_host_file,\
    get_site_domains_from_keywords,\
    unblock_site_host_method,list_blocked_sites,get_domain_info,run_pktmon_capture,extract_domains_from_pktmon
from flask import jsonify
import threading



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
    
    print(temp)
    
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

    download_speed,upload_speed = 0,0
    
    return {"download_speed":download_speed,"upload_speed":upload_speed}




@app.route('/block_sites')
def block_sites_view():
    
    sites = list_blocked_sites() 
    
    sites_info = get_domain_info(sites)
    
    threading.Thread(target=run_pktmon_capture, daemon=True).start()
    
    
    return render_template('web_protection.html',sites_info=sites_info)

@app.route('/visited-domains')
def visited_domains():
    domains = extract_domains_from_pktmon()
    print(domains)
    if not domains:
        return jsonify({"message": "No capture data available. Run /start-capture first."}), 404
    return jsonify(domains)

@app.route('/block_selected_site',methods=["POST"])
def block_selected_site_view(): 
    
    website = request.form.get("website").split(",")
    
    print(website)
    
    days = request.form.get("days")
    
    hours_from = request.form.get("timefrom")
    
    hours_to = request.form.get("timeto")
    
    justblock = request.form.get("justblock")
    
    print(days)
    print(hours_from)
    print(justblock)
    
    try:
        
        resp = block_sites_using_host_file(website)
        
    except Exception as err: 
        
        resp  = str(err)
        
    
    return f"<strong style='color:green'>{website} -> {resp}</strong>"

@app.route('/unblock_selected_site',methods=["POST"])
def unblock_selected_site_view():
    
    sites = request.form.get("website2").split(",")
    
    resp = unblock_site_host_method(sites)
    
                                                            
    
    
    return f"<strong style='color:green'>{sites} {resp}</strong>"
    
    

@app.route('/search_site_and_block',methods=["POST"])
def search_site_and_block_view(): 
    
    site_key_word = request.form.get("site_key_word")
    
    sites_domains = get_site_domains_from_keywords(site_key_word,2)
    
    return render_template('search_site.html',sites = sites_domains)
    
    
    
    