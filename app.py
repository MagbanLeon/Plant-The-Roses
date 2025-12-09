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
        value = plant()
        if value is not None:
            garden(value)
            return render_template('landing.html', un = session['username'], loaded = 1, flowerlink = 'static/currentflower.png')
        else:
            return render_template('landing.html', un = session['username'], loaded = 0)
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

        cursor = get_db().cursor()
        cursor.execute('SELECT * FROM GEEK WHERE Username = ? AND Password = ?', (username, password))
        account = cursor.fetchone()

        if account:
            value = plant()
            if value is not None:
                garden(value)
                return render_template('landing.html', un = session['username'], loaded = 1, flowerlink = 'static/currentflower.png')
            else:
                return render_template('landing.html', un = session['username'], loaded = 0)
        else:
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
        username = request.form['username']
        session['username'] = username
        password = request.form['password']
        dtabase = get_db()
        cursor = dtabase.cursor()
        cursor.execute("INSERT INTO GEEK (Username, Password, SavedImg) VALUES (?, ?, NULL)", (username, password))
        dtabase.commit()
    return render_template('landing.html', un = username, loaded = 1)

@app.route('/logout', methods = ['POST'])
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return render_template('login.html')

@app.route('/gumi', methods = ['GET', 'POST'])
def gumi():
    #if request.method == 'POST' and 'flower' in request.form:
    file = request.files['flower']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['save_path'], filename))
    
    if True:
        with open('local/'+ os.listdir(save_path)[0], 'rb') as file:
            image_data = file.read()
            get_db().cursor().execute("""
            UPDATE GEEK
            SET SavedImg = ?
            WHERE Username = ?;
            """, (image_data, session['username']))
            get_db().commit()
            remove(save_path)
        value = plant()
        if value is not None:
            garden(value)
            return render_template('landing.html', un = session['username'], loaded = 1, flowerlink = 'static/currentflower.png')
        else:
            return render_template('landing.html', un = session['username'], loaded = 0)
    else:
        return render_template('landing.html', un = session['username'], loaded = 1)
    
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

def plant():
    print("planting")
    cur = get_db().cursor()
    un = session['username']
    cur.execute("SELECT SavedImg FROM GEEK WHERE Username = ?", (un,))
    data = cur.fetchone()[0]
    return data

def garden(data):
    print("gardening")
    unroot() #gets rid of current image file
    with open('static/currentflower.png', 'wb') as file:
        file.write(data)

def unroot():
    print("unrooting")
    file = 'currentflower.png'
    location = '/workspaces/Plant-The-Roses/static'
    path = os.path.join(location, file)

    os.remove(path)
    print(f"{file} has been removed successfully")

app.run(debug=True, port=8080)