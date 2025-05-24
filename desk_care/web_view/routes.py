from flask import Flask,render_template,request
from pc_data.pc_info import get_cpu_battery,get_cpu_temperature,\
    get_cpu_performance,calculate_usage
from pc_data.web_protection import block_sites_using_host_file,\
    get_site_domains_from_keywords,\
    unblock_site_host_method,list_blocked_sites,get_domain_info,run_pktmon_capture,unblock_individual_domain_host_method

from pc_data.encryptions import encrypt_file_password_method
    
from pc_data.track_domains import *
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

    This function returns a dictionary containing the current CPU frequency data
    with the keys 'current', 'min', and 'max'. The data is obtained by calling
    the get_cpu_performance() function.

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

    This function uses the `get_upload_download_speed` function to obtain
    the current internet download and upload speeds and returns them as a
    dictionary with keys 'download_speed' and 'upload_speed'.

    Returns:
        dict: A dictionary containing the current download and upload speeds
        with the keys 'download_speed' and 'upload_speed'.
    """
    # Use the function to get the speeds
    # Initialize the download and upload speeds
    download_speed, upload_speed = get_upload_download_speed()

    # Return the speeds in a dictionary
    return {"download_speed": download_speed, "upload_speed": upload_speed}
    download_speed,upload_speed = 0,0
    
    return {"download_speed":download_speed,"upload_speed":upload_speed}






@app.route('/block_sites')
def block_sites_view():
    

    """
    Web page for managing blocked sites.

    This function renders a web page showing the current list of blocked
    sites. It also starts a thread to run the packet capture utility.

    Returns:
        str: The rendered HTML page.
    """

    sites = list_blocked_sites() 
    
    sites_info = get_domain_info(sites)
    
    threading.Thread(target=run_pktmon_capture, daemon=True).start()
    
    
    return render_template('web_protection.html',sites_info=sites_info)

@app.route('/start_packet_capture')
def start_packet_capture_view(): 
    

    """
    Web page for starting the packet capture utility.

    This function renders a web page after starting the packet capture utility.

    Returns:
        str: The rendered HTML page.
    """

    ensure_npcap()
    
    if is_sniffer_running(): 
        
        resp = "Tracker Already Running"
        
    start_sniffer()
    
    resp = "Started Tracking ---"
    
    return render_template('start_tracking.html',resp=resp,domains=sorted(visited_domains),n=len(visited_domains)) 


@app.route('/visited_domains')
def visited_domains_view(): 
    

    """
    Render a web page displaying a list of visited domains.

    This function renders the 'visited_domains_list.html' template, passing
    a sorted list of visited domains and their count.

    Returns:
        str: The rendered HTML page with visited domains.
    """


    return render_template("visited_domains_list.html",domains=sorted(visited_domains),n=len(visited_domains))
    
    

@app.route('/block_selected_site',methods=["POST"])
def block_selected_site_view(): 
    

    """
    Web page for blocking selected sites.

    This function renders a web page after blocking the specified website(s)
    using the host file method.

    Args:
        website (list): A list of website URLs to block.
        days (str): The number of days to block. If empty, block until manually
            unblocked.
        hours_from (str): The time to start blocking in the format "HH:MM".
        hours_to (str): The time to end blocking in the format "HH:MM".
        justblock (str): A flag to indicate if only blocking should be done
            without scheduling.

    Returns:
        str: The rendered HTML page with the status of the blocking operation.
    """
    

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
        
    sites = list_blocked_sites() 
    
    sites_info = get_domain_info(sites)
    
    return render_template("update_blocked_domains.html",sites_info=sites_info)

@app.route('/unblock_selected_site',methods=["POST"])
def unblock_selected_site_view():
    
    sites = request.form.get("website2").split(",")
    
    resp = unblock_site_host_method(sites)
    
                                                            
    
    
    return f"<strong style='color:green'>{sites} {resp}</strong>"

@app.route('/unblock_individual_domain/<domain>')
def unblock_individual_domain_view(domain):
    
    resp = unblock_individual_domain_host_method(domain)
    
    sites = list_blocked_sites() 
    
    sites_info = get_domain_info(sites)
    
    return render_template("update_blocked_domains.html",sites_info=sites_info)
    
    
    
    

@app.route('/search_site_and_block',methods=["POST"])
def search_site_and_block_view(): 
    
    site_key_word = request.form.get("site_key_word")
    
    sites_domains = get_site_domains_from_keywords(site_key_word,2)
    
    return render_template('search_site.html',sites = sites_domains)


@app.route('/encrypt_files')
def encrypt_files_view():
    
    return render_template('encrypt_files.html')

@app.route('/get_file_to_encrypt',methods=["POST"])

def get_file_to_encrypt_view():
    
    files = request.files.getlist("files")
    password = request.form.get("pass")
    
    responses = []
    
    for file in files:
        
        resp= encrypt_file_password_method(file,password)
        responses.append(resp)
        
    print(responses)
    
    return f"{responses} >>"
        
        
    
    
    
    

    
    
    
    
    
    
    
    