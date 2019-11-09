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
from db.insert_user_table import insert_users_db
from db.get_user_pw import get_user_pw_with_username
from model.user import User
from model.player import Player
result = []
@app.route("/")
def index():
    return render_template("home.html",methods=["POST","GET"])
@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password_form = request.form['password']
        passwd_from_db = get_user_pw_with_username(username) 
        print(passwd_from_db)
        if(password_form == passwd_from_db[0]):
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
        usr = User(username, password, True, False)
        insert_users_db(usr)
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
        player = Player(full_name, 0, age)
        insert_players_db(player, username, team_name)
        return render_template("profile.html")
    return render_template("profile.html", teams = teams)


@app.route("/players")
def all_players_page():
    players = []
    players = get_players_db()
    return render_template("players.html", players = players)    
@app.route("/teams")
def all_teams_page():
    teams = []
    teams = get_teams_db()
    print(teams[0])
    return render_template("teams.html", teams = teams)
if __name__ == "__main__":
    app.run(debug=True) 
