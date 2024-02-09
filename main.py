from flask import Flask, render_template, redirect, request
import flask_login
import pymysql
import pymysql.cursors


app = Flask(__name__)
app.secret_key = "something_secret" # Change this!

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
class User:
    is_authenticated = True
    is_anonymous = False
    is_active = True

    def __init__(self, id, username):
        self.username = username
        self.id = id

    def get_id(self):
        return str(self.id)
    


@login_manager.user_loader
def load_user(user_id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM `users` WHERE `id` = {user_id}")
    result = cursor.fetchone()
    cursor.close()
    conn.commit()

    if result is None:
        return None
    
    return User(result["id"], result["username"])



conn = pymysql.connect(
    database = "fmuntasir2_getgotApp",
    user = "fmuntasir2",
    password = "239442965",
    host = "10.100.33.60",
    cursorclass = pymysql.cursors.DictCursor
)



@app.route('/')
def landing_page():
    if flask_login.current_user.is_authenticated:
        return redirect('/feed')
        
    return render_template('land.html.jinja')



@app.route('/sign_up', methods =['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_email = request.form['new_email']
        new_password = request.form['new_password']
        cursor = conn.cursor()
        cursor.execute(f'INSERT INTO `users` (`username`, `email`, `password`) VALUES ("{new_username}", "{new_email}", "{new_password}");')
        cursor.close()
        conn.commit()
    return render_template('sign_up.html')


@app.route('/sign_in', methods =['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        cursor = conn.cursor()
        cursor.execute(f' SELECT * FROM `users` WHERE `username` = "{username}" ')
        result = cursor.fetchone()
        cursor.close()
        conn.commit()
        
        if password == result["password"]:
            user = load_user(result['id'])
            flask_login.login_user(user)
            return redirect('/feed')
    return render_template("sign_in.html")


@app.route('/feed')
@flask_login.login_required
def post_feed():
    return flask_login.current_user
