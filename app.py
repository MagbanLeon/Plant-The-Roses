# idk 2
# https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace
# it didnt work becuase you didnt pip install flask DUMBASS

from flask import Flask, render_template, g, request, session
from models import get_db
from controller import Controller
from models import Model

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def hello_world():
    return render_template('login.html')

@app.route("/login", methods = ['POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(username + " " + password)
        cursor = get_db().cursor()
        cursor.execute('SELECT * FROM GEEK WHERE Username = ? AND Password = ?', (username, password))
        account = cursor.fetchone()
        if account:
            print("um")
            return render_template('landing.html')
        else:
            msg = 'Incorrect username/password!'
            print("uokm")
    return render_template('login.html')

@app.route("/inbetween")
def inbetween():
    return render_template('register.html')

@app.route("/register", methods = ['POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(username + " " + password)
        dtabase = get_db()
        cursor = dtabase.cursor()
        cursor.execute("INSERT INTO GEEK (Username, Password) VALUES ('Mag', 'Mag')")
        dtabase.commit()
    return render_template('landing.html')
    
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

app.run(debug=True, port=8080)