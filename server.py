from flask import Flask, request,flash,session
from flask import render_template, redirect
import psycopg2 as dbapi2
from forms import LoginForm, RegisterForm
app = Flask(__name__)
app.secret_key = 'ITUCSDB1969'
from db.get_user_table import get_users_db
from db.get_db_url import get_db_url
from db.get_team_table import get_teams_db
from db.insert_player_table import insert_players_db
from db.get_player_table import get_players_db
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
            print(result)
            if(password_form == result[0]):
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

@app.route("/profile", methods=['POST','GET'])
def profile_sets():
    print("as")
    teams = []
    teams = get_teams_db()
    print("as")
    if request.method == 'POST':
        full_name = request.form['full_name']
        age = request.form['age']
        team_name = request.form['team_name']
        username = session['username']
        print(full_name, age, username, team_name)
        insert_players_db(full_name, age, username, team_name)
        return render_template("profile.html")
    return render_template("profile.html", teams = teams)


@app.route("/players")
def all_players_page():
    players = []
    players = get_players_db()
    print(players[0])
    return render_template("players.html", players = players)    
@app.route("/teams")
def all_teams_page():
    teams = []
    teams = get_teams_db()
    print(teams[0])
    return render_template("teams.html", teams = teams)
if __name__ == "__main__":
    app.run(debug=True) 
