# idk 2
# https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace
# it didnt work becuase you didnt pip install flask DUMBASS

from flask import Flask, render_template, g
from models import get_db

app = Flask(__name__)

@app.route("/")
def hello_world():
    cur = get_db().cursor()
    return render_template('landing.html')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

app.run(debug=True)