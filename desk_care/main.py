from flask import Flask,render_template 
from flaskwebgui import FlaskUI
import socket

app = Flask(__name__)

UI = FlaskUI(app=app,server="flask",width=1000,height=1000)

@app.route('/')
def home_page(): 
    
    
    return render_template('index.html')




if __name__=='__main__': 
    
    app.run(debug=True)
    
    #UI.run()