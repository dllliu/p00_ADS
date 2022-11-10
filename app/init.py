from flask import Flask             #facilitate flask webserving
from flask import render_template, request   #facilitate jinja templating
from flask import session, redirect, url_for, make_response        #facilitate form submission
import os 
import db_tools

#the conventional way:
#from flask import Flask, render_template, request

#redirect url to the specific links from the html templates

app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32)
@app.route('/')
def index():
    if 'username' in session:
        return redirect("/home")
    return render_template('login.html') #edit

@app.route('/login', methods = ['GET','POST'])
def login():
    #Check if it already exists in database and render home page if it does
    #otherwise redirect to error page which will have a button linking to the login page
    username = request.form.get('username')
    password = request.form.get('password')
    if db_tools.verify_account(username,password):
        session['username'] = username
        session['password'] = password
        return redirect("/home")
    else:
        resp = make_response(render_template('error.html',msg = "username or password is not correct"))
        return resp


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    '''
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    '''
    print("creating account")
    if request.method == 'POST':
        userIn = request.form.get('username')
        passIn = request.form.get('password') 
        #print(userIn)
        #print(passIn)
        if db_tools.add_account(userIn, passIn) == -1:
            return f"account with username {userIn} already exists"
        else:
            return f"Successfully added {userIn}"
            #return redirect("/login")

        return resp
    return redirect(url_for('index'))
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/home')
def home():
    username = session['username']
    password = session['password']
    if db_tools.verify_account(username, password):
        viewable_pages, editable_pages = db_tools.get_user_stories(username)[0], db_tools.get_user_stories(username)[1]
        print(viewable_pages)
        return render_template("home_page.html", username = username,
        viewable_stories = viewable_pages, editable_stories = editable_pages)
        
    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    print(db_tools.get_table_list("UserInfo"))
    app.run()
    #db.commit()
    #db.close()