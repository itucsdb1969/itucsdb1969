from flask import Flask, request,flash,session
from flask import render_template, redirect
import psycopg2 as dbapi2
from forms import LoginForm, RegisterForm
app = Flask(__name__)
app.secret_key = 'ITUCSDB1969 SA'
from db.get_user_table import get_users_db
from db.get_db_url import get_db_url
result = []
@app.route("/")
def index():
    return render_template("home.html",methods=["POST","GET"])
@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/login", methods=['POST','GET'])
def login():
    result = []
    if request.method == "POST":
        username = request.form['username']
        password_form = request.form['password']
        url = get_db_url()
        with dbapi2.connect(url) as connection: 
            cursor = connection.cursor()
            statement = """select password from users 
                    where name = %s"""
            cursor.execute(statement, [username])
            result = cursor.fetchone()
            cursor.close()
            if(password_form == result):
                session['username'] = username
                return render_template("home.html")
            else:
                return render_template("login.html", error= "Invalid Password Error!")            
    return render_template("login.html")


@app.route("/register", methods=['POST', 'GET'])
def register_page():
    print("sa")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # print(username, password)
        url = get_db_url() #"dbname='postgres' user='postgres' host='localhost' password='123456'"
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        statement = """insert into users(name, password, is_active, is_admin) values(%s , %s , true , false);"""
        cursor.execute(statement, (username,password))
        connection.commit()
        cursor.close()
        return render_template("home.html")
    return render_template("register.html")

@app.route("/logout", methods=['POST','GET'])
def logout():
    session.pop('username', None)
    return render_template("home.html")

@app.route("/players")
def all_players_page():
    return render_template("players.html")    
@app.route("/teams")
def all_teams_page():
    return render_template("teams.html")
if __name__ == "__main__":
    app.run(debug=True) 
