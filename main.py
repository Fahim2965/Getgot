from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    user_name = "goodjob"
    
    return render_template("land.html.jinja", user_name = user_name)

@app.route('/ping')
def bub():
    return "<h1> Pong <h1>"
