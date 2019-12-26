Parts Implemented by Hasan Hüseyin KAÇMAZ
================================

Functions in server.py
------------

login()
^^^^^^^^
.. code-block:: python
def login():
    if request.method == "POST":
        username = request.form['username']
        password_form = request.form['password']
        if not username or not password_form:
            return render_template("login.html", error="Username/Password can not be empty!")
        passwd_from_db = get_user_pw_with_username(username)
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

This code block contains the login page logic.

register_page()
^^^^^^^^
.. code-block:: python
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
            usr = User(username, password, True, False)
            insert_users_db(usr)
            flash('You have successfully created an account, now you can login')
            return render_template("home.html")
        except psycopg2.errors.UniqueViolation:
            return render_template("register.html", error="Username already exists, pick different one!")
    return render_template("register.html")

This code block contains the register page logic. Every pass is first crypted using SHA256, then stored as
hash digest in the database.

profile_sets()
^^^^^^^^
.. code-block:: python
def profile_sets():
    teams = get_teams_db()
    status = int(check_profile_exists(session['username']))
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

This page creates a player, if created updates this player and checks for user session.

logout()
^^^^^^^^
.. code-block:: python
def logout():
    session.pop('username', None)
    flash("You have successfully logged out!")
    return render_template("home.html")

This code block helps user to logout, using sessions for authentication.

delete_player()
^^^^^^^^
.. code-block:: python
def delete_player():
    usrname = session['username']
    flash("You have successfully deleted your player profile!")
    delete_players_db(usrname)
    return render_template("home.html")

This function checks if a player exists for a user in database, then calls the delete_players_db function from database.

my_account()
^^^^^^^^
.. code-block:: python
def my_account():
    if request.method == 'GET':
        return render_template("my_account.html")
    if request.method == 'POST':
        password = request.form['new_password']
        c_password = request.form['new_password_conf']
        if password != c_password:
            return render_template("my_account.html", error="Passwords do not match!")
        password = hashlib.sha256(password.encode()).hexdigest()
        flash("Password successfully updated!")
        update_users_db(session['username'], password)
        return render_template("home.html")


@app.route("/delete_my_account", methods=['POST'])
def delete_my_account():
    flash("User successfully deleted!")
    delete_users_db(session['username'])
    session.pop('username', None)
    return render_template("home.html")

This functions helps users to change/update passwords, and delete accounts

upload_image()
^^^^^^^^
.. code-block:: python
def upload_image():
    if request.method=='POST':
        if request.files:
            image = request.files["image"]
            print(image)
    return render_template("my_account.html")

This function is partially implemented for users to insert a profile picture for themselves.


teams()
^^^^^^^^
.. code-block:: python
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

def delete_team():
    if request.method == 'POST':
        team_name = request.form['delete_team']
        delete_team_db(team_name)
    return redirect("teams")

def update_team():
    if request.method == 'POST':
        old_team_name = request.form['old_team_name']
        new_team_name = request.form['new_team_name']
        update_teams_db(new_team_name, old_team_name)
    return redirect("teams")

These 3 function is implemented for CRUD operation for team table.

team()
^^^^^^^^
.. code-block:: python
def team():
    if request.method == 'POST':
        team_id = request.form['team_id']
        players = get_team_players_with_team_id(team_id)
        return render_template("team.html", infos=players)
    if request.method == 'GET':
        return render_template("team.html")

This function lists all players for a team.




matches()
^^^^^^^^
.. code-block:: python
def matches():
    if request.method == 'POST':
        teams = get_teams_db()
        match = Match(request.form['team_home'], request.form['team_away'])
        match_id = insert_match_db(match)
        stadiums = get_stadiums_db()
        stadium_id = get_stad_id_with_stad_name(request.form['stadium_name'])
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
        return render_template("matches.html", matchs=matchs, teams=teams, stadiums=stadiums)

def delete_matches():
    if request.method == 'POST':
        name = request.form['delete_match']
        delete_appointment_db(name)
    return redirect("matches")

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

These 3 function is implemented for calling CRUD operation functions for appointment table, also reflects match and team tables.



stadiums()
^^^^^^^^
.. code-block:: python
def stadiums():
    if request.method == 'GET':
        stadiums = get_stadiums_db()
        return render_template("stadiums.html", stadiums=stadiums)
    if request.method == 'POST':
        if not request.form['stadium_name']:
            stadiums = get_stadiums_db()
            return render_template("stadiums.html", stadiums=stadiums, error="Stadium name can not be empty!")
        stadium_name = request.form['stadium_name']
        stadium = Stadium(stadium_name)
        try:
            insert_stadiums_db(stadium)
            flash("Stadium successfully added!")
            stadiums = get_stadiums_db()
            return render_template("stadiums.html", stadiums=stadiums)
        except psycopg2.errors.UniqueViolation:
            stadiums = get_stadiums_db()
            return render_template("stadiums.html", stadiums=stadiums, error="Stadium name must be different!")

def delete_stadiums():
    stadium_name = request.form['stadium_name']
    delete_stadium_db(stadium_name)
    stadiums = get_stadiums_db()
    flash("Stadium " + stadium_name + " successfully deleted!")
    return render_template("stadiums.html", stadiums=stadiums)

def update_stadiums():
    new_stad_name = request.form['new_stadium_name']
    update_stadiums_db(request.form['old_stadium_name'], new_stad_name)
    stadiums = get_stadiums_db()
    flash("Stadium name successfully updated!")
    return render_template("stadiums.html", stadiums=stadiums)

These 3 function is implemented for calling CRUD operation functions for stadium table.
