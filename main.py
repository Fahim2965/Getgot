from flask import Flask, render_template, redirect
import pymysql
import pymysql.cursors


app = Flask(__name__)

conn = pymysql.connect(
    database = "fmuntasir2_getgotApp",
    user = "fmuntasir2",
    password = "239442965",
    host = "10.100.33.60",
    cursorclass = pymysql.cursors.DictCursor
)

@app.route('/')
def index():
    return render_template('land.html.jinja')

@app.route('/sign_up', methods =['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_username = request.form["username"]
        #todos.append(new_todo)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO `todos` (`description`) VALUES ('{new_todo}')")
        cursor.close()
        conn.commit()

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `todos` ORDER BY `complete`")
    results = cursor.fetchall()
    cursor.close()

@app.route('/sign_in', methods =['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        cursor = conn.cursor()


        cursor.execute(f""" SELECT * FROM `users` WHERE `username` = '{username}' """)

        user = cursor.fetchone()


        cursor.close()
        conn.commit()
        
        if password == user["password"]:
            return redirect('/feed')

    return render_template("sign-in.html")