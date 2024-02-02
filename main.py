from flask import Flask, render_template
import pymysql
import pymysql.cursors
from pprint import pprint as print
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

@app.route('/')
def index():
    user_name = "goodjob"
    
    return render_template("land.html.jinja", user_name = user_name)

@app.route('/ping')
def bub():
    return "<h1> Pong <h1>"

conn = pymysql.connect(
    database = "fmuntasir2_getgotApp",
    user = "fmuntasir2",
    password = "239442965",
    host = "10.100.33.60",
    cursorclass = pymysql.cursors.DictCursor
)

@app.route('/', methods =['GET', 'POST'])
@auth.login_required
def index():
    if request.method == 'POST':
        new_todo = request.form["users"]
        #todos.append(new_todo)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO `todos` (`description`) VALUES ('{new_todo}')")
        cursor.close()
        conn.commit()

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `todos` ORDER BY `complete`")
    results = cursor.fetchall()
    cursor.close()
