# idk 2
# https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

app.run(debug=True)