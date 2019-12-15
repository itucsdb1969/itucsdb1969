import psycopg2
import hashlib 
from flask import Flask, request, session, flash
from flask import render_template, redirect
from model.user import User
from model.player import Player
from model.team import Team
from model.match import Match
from model.appointment import Appointment
from model.stadium import Stadium
from db.user.insert_user_table import insert_users_db
from db.user.get_user_pw import get_user_pw_with_username
from db.utils.get_profile_status import check_profile_exists
from db.match.insert_match_table import insert_match_db
from db.player.insert_player_table import insert_players_db
from db.player.get_player_table import get_players_db
from db.player.update_player_table import update_players_db
from db.player.delete_player_table import delete_players_db
from db.player.get_user_player_table import get_player_with_username
from db.team.get_team_table import get_teams_db
from db.team.get_team_player_table import get_team_players_with_team_id
from db.team.insert_team_table import insert_teams_db
from db.stadium.get_stadium_table import get_stadiums_db
from db.stadium.get_stadium_id import get_stad_id_with_stad_name
from db.stadium.delete_stadium_table import delete_stadium_db
from db.stadium.insert_stadium_table import insert_stadiums_db
from db.appointment.insert_appointment_table import insert_appointments_db
from db.appointment.get_appointment_table import get_appointments_db
from db.appointment.update_appointment_table import update_appointments_db
app = Flask(__name__)
app.secret_key = 'ITUCSDB1969'
result = []


@app.route("/")
def index():
    return render_template("home.html", methods=["POST", "GET"])


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password_form = request.form['password']
        if not username or not password_form:
            return render_template("login.html", error="Username/Password can not be empty!")
        passwd_from_db = get_user_pw_with_username(username) 
        # print(passwd_from_db)
        if passwd_from_db:
            password_form = hashlib.sha256(password_form.encode()).hexdigest()
            if password_form == passwd_from_db[0]:
                session['username'] = username
                flash("You have successfully logged in!")
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
        c_password = request.form['confirm-password']
        if not username or not password or not c_password:
            return render_template("register.html", error="Username/Password can not be empty!")
        if password != c_password:
            return render_template("register.html", error="Passwords do not match!")
        try:
            password = hashlib.sha256(password.encode()).hexdigest()
            print(password)
            usr = User(username, password, True, False)
            insert_users_db(usr)
            flash('You have successfully created an account, now you can login')
            return render_template("home.html")
        except psycopg2.errors.UniqueViolation:
            # print("Username already exists, pick different one!")
            return render_template("register.html", error="Username already exists, pick different one!")
    return render_template("register.html")


@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.pop('username', None)
    flash("You have successfully logged out!")
    return render_template("home.html")


@app.route("/profile", methods=['POST', 'GET'])
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
            try:
                update_players_db(player, username, team_name)
                flash("You have successfully updated your player profile!")
            except psycopg2.errors.InvalidTextRepresentation:
                return render_template("profile.html", teams=teams, status=status, error="Name/Age not valid!")
        else:
            try:
                insert_players_db(player, username, team_name)
                flash("You have successfully created your player profile!")
                status = 1
            except psycopg2.errors.InvalidTextRepresentation:
                return render_template("profile.html", teams=teams, status=status, error="Name/Age not valid!")
    return render_template("profile.html", teams=teams, status=status)


@app.route("/delete", methods=['POST'])
def delete_player():
    usrname = session['username']
    flash("You have successfully deleted your player profile!")
    delete_players_db(usrname)
    return render_template("home.html")


@app.route("/players")
def all_players_page():
    players = []
    players = get_players_db()
    print("players:", players)
    return render_template("players.html", players=players)


@app.route("/teams", methods=['GET', 'POST'])
def all_teams_page():
    if request.method == 'POST':
        if not request.form['team_name']:
            teams = get_teams_db()
            return render_template("teams.html", teams=teams, error="Team name can not be empty!")
        try:
            team = Team(request.form['team_name'], request.form['rating'], "yes")
            insert_teams_db(team)
            teams = get_teams_db()
            flash("Team successfully added!")
        except psycopg2.errors.UniqueViolation:
            teams = get_teams_db()
            return render_template("teams.html", teams=teams, error="Team name must be unique!")
        return render_template("teams.html", teams=teams)
    elif request.method == 'GET':
        teams = get_teams_db()
        return render_template("teams.html", teams=teams)


@app.route("/team", methods=['GET', 'POST'])
def team():
    if request.method == 'POST':
        team_id = request.form['team_id']
        players = get_team_players_with_team_id(team_id)
        return render_template("team.html", infos=players)
    if request.method == 'GET':
        return render_template("team.html")


@app.route("/matches", methods=['GET', 'POST'])
def matches():
    if request.method == 'POST':
        teams = get_teams_db()
        match = Match(request.form['team_home'], request.form['team_away'])
        match_id = insert_match_db(match)
        stadiums = get_stadiums_db()
        stadium_id = get_stad_id_with_stad_name(request.form['stadium_name'])
        print(request.form['match_date'])
        appointment = Appointment(request.form['appointment_name'], match_id, stadium_id, request.form['start_time'], request.form['end_time'], request.form['match_date'])
        if not request.form['appointment_name']:
            matchs = get_appointments_db()
            return render_template("matches.html", matchs=matchs, teams=teams, stadiums=stadiums, error="Appointment name can not be empty!")
        try:
            insert_appointments_db(appointment)
            flash("Appointment successfully created!")
            matchs = get_appointments_db()
        except psycopg2.errors.UniqueViolation:
            matchs = get_appointments_db()
            return render_template("matches.html", matchs=matchs, teams=teams, stadiums=stadiums, error="Appointment name already exists!")
        return render_template("matches.html", matchs=matchs, teams=teams, stadiums=stadiums)
    if request.method == 'GET':
        teams = get_teams_db()
        matchs = get_appointments_db()
        stadiums = get_stadiums_db()
        print(matchs)
        return render_template("matches.html", matchs=matchs, teams=teams, stadiums=stadiums)

@app.route("/stadiums", methods=['GET', 'POST'])
def stadiums():
    stadiums = []
    if(request.method == 'GET'):
        stadiums = get_stadiums_db()
        print(stadiums)
        return render_template("stadiums.html", stadiums = stadiums)
    if(request.method == 'POST'):
        stadium_name = request.form['stadium_name']
        stadium = Stadium(stadium_name)
        insert_stadiums_db(stadium)
        stadiums = get_stadiums_db()
        return render_template("stadiums.html", stadiums = stadiums)
@app.route("/delete_stadiums", methods=['POST'])
def delete_stadiums():
    stadium_name = request.form['stadium_name'] 
    print("aslkdjaşklsdjaşklsd", stadium_name)
    delete_stadium_db(stadium_name)
    stadiums = get_stadiums_db()
    print(stadiums, request.form['stadium_name'])
    return render_template("stadiums.html", stadiums= stadiums)
@app.route("/edit_matches", methods=['GET', 'POST'])
def edit_matches():
    username = request.form['user_name']
    if get_player_with_username(username):
        update_appointments_db(request.form['match_id'], request.form['user_name'])
    else:
        teams = get_teams_db()
        matchs = get_appointments_db()
        stadiums = get_stadiums_db()
        return render_template("matches.html", matchs=matchs, teams=teams, stadiums=stadiums, error="You need to create a player profile!")
    return redirect("matches")
if __name__ == "__main__":
    app.run(debug=True) 
