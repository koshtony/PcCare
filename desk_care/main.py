from web_view import app,UI
from pc_data.track_domains import ensure_npcap

if __name__=='__main__': 
    
    ensure_npcap()
    #app.run(debug=True)
    
    UI.run()