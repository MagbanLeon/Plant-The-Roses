from flask import render_template, redirect, url_for

class View:
    def loadLanding(username, whetherLoaded, boquet):
        return render_template('landing.html', un = username, loaded = whetherLoaded, flowerlink = boquet)
    def loadLogin():
        return render_template('login.html')
    def loadRegister():
        return render_template('register.html')
    def deaultRedirect():
        return redirect(url_for('hello_world'))