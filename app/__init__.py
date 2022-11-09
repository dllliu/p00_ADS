# ADS: Ayman Habib, Sam Lubelsky, Daniel Liu
# Softdev pd02
# k19
# 2022-11-03
# time spent: 

from flask import Flask             #facilitate flask webserving
from flask import render_template, make_response   #facilitate jinja templating
from flask import request, session, redirect, url_for          #facilitate form submission
import os 

#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32)

@app.route("/addToStory")
def addToStory():
    newText = request.form.get("NewText")
    

