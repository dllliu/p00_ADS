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
    elif request.method == 'POST':
        if request.form['submit_button'] == "Create New Account":
            return render_template("create_account.html")
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
    #print("creating account")
    if request.method == 'POST':
        userIn = request.form.get('username')
        passIn = request.form.get('password') 
        #print(userIn)
        #print(passIn)
        if db_tools.add_account(userIn, passIn) == -1:
            return f"account with username {userIn} already exists"
        else:
            return render_template("sign_up_success.html")
            #return redirect("/login")
    return redirect(url_for('index'))
    
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect("/login")
    username = session['username']
    password = session['password']
    if db_tools.verify_account(username, password):
        viewable_pages, editable_pages = db_tools.get_user_stories(username)[0], db_tools.get_user_stories(username)[1]
        print("viewable pages:" + str(viewable_pages))
        return render_template("home_page.html", username = username,
        viewable_stories = viewable_pages, editable_stories = editable_pages)

@app.route('/view')
def view():
    if verify_session():
        storyname = request.args.get("storyName")
        #print("storyName: " + storyname)
        storyInfo = db_tools.get_story_info(storyname)
        if storyInfo == -1:
            return render_template("error.html", msg="Story is Not in Database")
        fullText = storyInfo[0]
        contributors = storyInfo[2]
        if session['username'] in contributors.split(','):
            return render_template("story_tmplt.html",fullText = fullText,storyname = storyname)
    return render_template("error.html", msg="session could not be verified")
@app.route('/edit')
def edit():
    #print(session)
    if verify_session():
        storyName = request.args.get("storyName")
        storyInfo = db_tools.get_story_info(storyName)
        #print(storyInfo)
        lastAdded = storyInfo[1]
        contributors = storyInfo[2].split(",")
        if session['username'] not in contributors:
            return render_template('edit.html', storyName = storyName, storyText = lastAdded)
        else:
            return render_template("error.html", msg= "user has already edited story")
    else:
        return render_template("error.html", msg="session could not be verified")
    
@app.route("/make_edit", methods = ['POST'])
def make_edit():
    if verify_session():
        storyName = request.form.get("storyName")
        newAddition = request.form.get("newText")
        print("Editing Story:")
        print(storyName, newAddition, session['username'])
        db_tools.edit_story(storyName, newAddition, session['username'])
        return redirect("/")
    else:
        return render_template("error.html", msg = "session could not be verified")

def verify_session():
    if 'username' in session and 'password' in session:
        if db_tools.verify_account(session['username'], session['password']):
            return True
    return False

@app.route('/create_story', methods=['GET', 'POST'])
def create_story():
    if verify_session():
        username = session['username']
        storyName = request.form.get('storyName')
        newText = request.form.get('newText')
        if db_tools.add_story(storyName,newText,username) != -1:
            return render_template("create.html",storyName = storyName)
        else:
            if db_tools.story_exists(storyName):
                return "Story Already Added"
            else:
                return "Story Addition Not Successful. Try Again"
    else:
        return render_template("error.html", msg="session could not be verified")
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    print(db_tools.get_table_list("StoryInfo"))
    app.run()
    #db.commit()
    #db.close()
