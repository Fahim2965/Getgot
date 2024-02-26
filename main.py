from flask import Flask, render_template, redirect, request, g
import flask_login
import pymysql
import pymysql.cursors


app = Flask(__name__)
app.secret_key = "2024ULX2023" # Change this!


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
    cursor = get_db().cursor()
    cursor.execute(f"SELECT * FROM `users` WHERE `id` = {user_id}")
    result = cursor.fetchone()
    cursor.close()
    get_db().commit()

    if result is None:
        return None
    
    return User(result["id"], result["username"])



def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user="YOUR_USERNAME",
        password="YOUR_PASSWORD",
        database="YOUR_DATABASE_NAME",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db    



@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''    
    if hasattr(g, 'db'):
        g.db.close()




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
        cursor = get_db().cursor()
        cursor.execute(f'INSERT INTO `users` (`username`, `email`, `password`) VALUES ("{new_username}", "{new_email}", "{new_password}");')
        cursor.close()
        get_db().commit()
    return render_template('sign_up.html')



@app.route('/sign_in', methods =['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        cursor = get_db().cursor()
        cursor.execute(f' SELECT * FROM `users` WHERE `username` = "{username}" ')
        result = cursor.fetchone()
        cursor.close()
        get_db().commit()
        
        if password == result["password"]:
            user = load_user(result['id'])
            flask_login.login_user(user)
            return redirect('/feed')
    return render_template("sign_in.html")



@app.route('/feed', methods=['GET', 'POST'])
@flask_login.login_required
def post_feed():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM `Posts` INNER JOIN `User` ON `Posts`.user_id = `User`.ID")
    results = cursor.fetchall()
    cursor.close()
    return render_template("feed.html.jinja", posts = results)
    return flask_login.current_user



@app.route('/post', methods=['GET', 'POST'])
@flask_login.login_required
def post():
    description = request.form['description']
    user_id = flask_login.current_user.id
    cursor = get_db().cursor()
    cursor.execute(f"INSERT INTO `Posts` (`description`, `user_id`) VALUES ('{description}', '{user_id}')")
    cursor.close()
    get_db().commit
    return redirect("/feed")