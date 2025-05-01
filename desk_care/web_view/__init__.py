from flask import Flask,render_template 
from flaskwebgui import FlaskUI

app = Flask(__name__,template_folder='templates')

UI = FlaskUI(app=app,server="flask",width=1000,height=1000) 

from web_view import routes
