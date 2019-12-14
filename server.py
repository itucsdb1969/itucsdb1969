from flask import Flask, request, session
from flask import render_template
from db.team.get_team_table import get_teams_db
from db.player.insert_player_table import insert_players_db
from db.player.get_player_table import get_players_db
from db.user.insert_user_table import insert_users_db
from db.user.get_user_pw import get_user_pw_with_username
from db.player.update_player_table import update_players_db
from db.utils.get_profile_status import check_profile_exists
from db.player.delete_player_table import delete_players_db
from model.user import User
from model.player import Player
from model.team import Team
from model.match import Match
from db.team.get_team_id import get_team_id_with_teamname
from db.team.get_team_player_table import get_team_players_with_team_id
from db.team.insert_team_table import insert_teams_db
from db.match.insert_match_table import insert_match_db
from db.match.get_match_table import get_match_db
app = Flask(__name__)
app.secret_key = 'ITUCSDB1969'
result = []


@app.route("/")
def index():
    return render_template("home.html",methods=["POST", "GET"])


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password_form = request.form['password']
        passwd_from_db = get_user_pw_with_username(username) 
        # print(passwd_from_db)
        if passwd_from_db:
            if password_form == passwd_from_db[0]:
                session['username'] = username
                return render_template("home.html")
            else:
                return render_template("login.html", error= "Invalid Password Error!")
        else:
            return render_template("login.html", error= "Invalid Username Error!")            
    return render_template("login.html")


@app.route("/register", methods=['POST', 'GET'])
def register_page():
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
    teams = []
    teams = get_teams_db()
    status = int(check_profile_exists(session['username']))
    # print("status: ", status)
    if request.method == 'POST':
        full_name = request.form['full_name']
        age = request.form['age']
        team_name = request.form['team_name']
        username = session['username']
        player = Player(full_name, 0, age)
        if status == 1:
            print("updated")
            update_players_db(player, username, team_name)
        else:
            insert_players_db(player, username, team_name)
            status = 1
        return render_template("profile.html", teams=teams, status=status)
    return render_template("profile.html", teams=teams, status=status)


@app.route("/delete", methods=['POST'])
def delete_player():
    usrname = session['username']
    delete_players_db(usrname)
    return render_template("home.html")


@app.route("/players")
def all_players_page():
    players = []
    players = get_players_db()
    print("players:", players)
    return render_template("players.html", players = players)


@app.route("/teams", methods=['GET','POST'])
def all_teams_page():
    if request.method == 'POST':
        print(request.form['team_name'])
        team = Team(request.form['team_name'], request.form['rating'], "yes")
        insert_teams_db(team)
        teams = []
        teams = get_teams_db()
        return render_template("teams.html",teams = teams)
    elif request.method == 'GET':
        teams = []
        teams = get_teams_db()
        print(teams[0])
        return render_template("teams.html", teams = teams)

@app.route("/team", methods=['GET','POST'])
def team():
    if request.method == 'POST':
        team_id = request.form['team_id']
        print("*************")
        print(team_id)
        players = get_team_players_with_team_id(team_id)
        return render_template("team.html", infos = players)
    if request.method == 'GET':
        return render_template("team.html")
@app.route("/matches", methods= ['GET', 'POST'])
def matches_page():
    if request.method == 'POST':
        teams = []
        teams = get_teams_db()
        match = Match(request.form['team_home'], request.form['team_away'])
        insert_match_db(match)
        matchs = []
        matchs = get_match_db()
        return render_template("matches.html", matchs = matchs, teams = teams)
    if request.method == 'GET':
        teams = []
        teams = get_teams_db()
        matchs = []
        matchs = get_match_db()
        return render_template("matches.html", matchs = matchs, teams = teams)
if __name__ == "__main__":
    app.run(debug=True) 
