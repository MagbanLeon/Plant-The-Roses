from models import Model
from view import View
from flask import Flask, render_template, g, request, session
import os
from werkzeug.utils import secure_filename

class Controller:
    app = None
    def __init__(self) -> None:
        self.m = Model()
        self.v = View()
        # self.app = Flask(__name__)

        # with self.app.app_context():
        self.app = Flask(__name__)
        self.app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
        self.save_path = '/workspaces/Plant-The-Roses/local'
        self.app.config['save_path'] = self.save_path

        self.app.run(debug=True, port=8080)

    @app.route("/", methods = ['GET', 'POST'])
    def hello_world(self):
        if 'username' in session:
            value = self.m.plant(session['username'])
            if value is not None:
                self.m.garden(value)
                return self.v.loadLanding(session['username'], 1, 'static/currentflower.png')
            else:
                return self.v.loadLanding(session['username'], 0, 'static/currentflower.png')
        else:
            return self.v.loadLogin()
        
    @app.route("/login", methods = ['POST'])
    def login(self):
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']

            session['username'] = username
            account = self.m.verifyAccount(username, password)

            if account:
                value = self.m.plant()
                if value is not None:
                    self.m.garden(value)
                    return self.v.loadLanding(session['username'], 1, 'static/currentflower.png')
                else:
                    return self.v.loadLanding(session['username'], 0, 'static/currentflower.png')
            else:
                return self.v.loadLogin()

    @app.route("/inbetween", methods = ['GET', 'POST'])
    def inbetween(self):
        if request.method == 'POST':
            session['username'] = request.form['username']
            return self.v.deaultRedirect()
        return self.v.loadRegister()

    @app.route("/inbetween2", methods = ['GET', 'POST'])
    def inbetween2(self):
        if request.method == 'POST':
            session['username'] = request.form['username']
            return self.v.deaultRedirect()
        return self.v.loadLanding()

    @app.route("/register", methods = ['POST'])
    def register(self):
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            session['username'] = username

            self.m.addAccount(username, password)
        return render_template('landing.html', un = username, loaded = 1)

    @app.route('/logout', methods = ['POST'])
    def logout(self):
        # remove the username from the session if it's there
        session.pop('username', None)
        return self.v.loadLogin()

    @app.route('/gumi', methods = ['GET', 'POST'])
    def gumi(self):
        #if request.method == 'POST' and 'flower' in request.form:
        file = request.files['flower']
        filename = secure_filename(file.filename)
        file.save(os.path.join(self.app.config['save_path'], filename))
        
        if True:
            self.m.addImage(file)
            value = self.m.plant()
            if value is not None:
                self.m.garden(value)
                return self.v.loadLanding(session['username'], 1, 'static/currentflower.png')
            else:
                return self.v.loadLanding(session['username'], 0, 'static/currentflower.png')
    @app.teardown_appcontext
    def close_connection(self):
        self.m.close()