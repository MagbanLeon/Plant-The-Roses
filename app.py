# idk 2
# https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace
# it didnt work becuase you didnt pip install flask DUMBASS

from flask import Flask, render_template, g, request, session, redirect, url_for
from models import get_db
from controller import Controller
from models import Model
import os, shutil
from os import listdir
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
save_path = '/workspaces/Plant-The-Roses/local'
app.config['save_path'] = save_path

@app.route("/", methods = ['GET', 'POST'])
def hello_world():
    if 'username' in session:
        return render_template('landing.html', un = session['username'])
    else:
        return render_template('login.html')

@app.route("/login", methods = ['POST'])
def login():
    # if request.method == 'POST':
    #     session['username'] = request.form['username']
    #     return redirect(url_for('hello_world'))
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        session['username'] = username
        password = request.form['password']
        print(username + " " + password)
        cursor = get_db().cursor()
        cursor.execute('SELECT * FROM GEEK WHERE Username = ? AND Password = ?', (username, password))
        account = cursor.fetchone()
        print(account)
        if account:
            print("um")
            return render_template('landing.html', un = username)
        else:
            msg = 'Incorrect username/password!'
            print("uokm")
    return render_template('login.html')

@app.route("/inbetween", methods = ['GET', 'POST'])
def inbetween():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('hello_world'))
    return render_template('register.html')

@app.route("/inbetween2", methods = ['GET', 'POST'])
def inbetween2():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('hello_world'))
    return render_template('login.html')

@app.route("/register", methods = ['POST'])
def register():
    # if request.method == 'POST':
    #     session['username'] = request.form['username']
    #     return redirect(url_for('hello_world'))
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        print("hello?")
        username = request.form['username']
        session['username'] = username
        password = request.form['password']
        print(username + " " + password)
        dtabase = get_db()
        cursor = dtabase.cursor()
        cursor.execute("INSERT INTO GEEK (Username, Password, SavedImg) VALUES (?, ?, NULL)", (username, password))
        dtabase.commit()
    return render_template('landing.html', un = username)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return render_template('login.html')

@app.route('/gumi', methods = ['GET', 'POST'])
def gumi():
    un = session['username']
    #if request.method == 'POST' and 'flower' in request.form:
    file = request.files['flower']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['save_path'], filename))
    
    if True:
        with open('local/'+ os.listdir(save_path)[0], 'rb') as file:
            print("working?")
            image_data = file.read()
            get_db().cursor().execute("""
            UPDATE GEEK
            SET SavedImg = ?
            WHERE Username = ?;
            """, (image_data, un))
            get_db().commit()
            remove(save_path)
        return render_template('landing.html', un = session['username'])
    else:
        return render_template('landing.html', un = session['username'])
    
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def remove(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

app.run(debug=True, port=8090)