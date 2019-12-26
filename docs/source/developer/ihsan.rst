Parts Implemented by İhsan SOYDEMİR
================================

Functions in db
------------

user()
^^^^^^^^
.. code-block:: python
def insert_appointments_db(appointment):
    query = "INSERT INTO APPOINTMENT (name, match_id, stadium_id, start_time, end_time, date) VALUES(%s, %s, %s, %s, %s, %s)"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (appointment.name, appointment.match_id, appointment.stadium_id, appointment.start_time, appointment.end_time, appointment.date, ))
        cursor.close()
        return True
def update_appointments_db(appointment_id, username):
    user_id = get_user_id_with_username(username)
    query = """	UPDATE MATCH SET
                 team2_id = (select team_id from player where user_id = %s)
                 WHERE match_id = (select match_id from APPOINTMENT
                 where appointment_id = %s)"""
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, appointment_id, ))
        cursor.close()
        return True
def get_appointments_db():
    query = """select a.appointment_id, a.name, t1.name, t2.name, s.name, a.start_time, a.end_time, a.date
	            from appointment as a, match as m, stadium as s, team as t1, team as t2
                where (m.match_id = a.match_id AND
			    a.stadium_id = s.stadium_id AND
			    (( m.team1_id = t1.team_id AND m.team2_id = t2.team_id ) ) )"""
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        appointments = cursor.fetchall()
        cursor.close()
        return appointments
def delete_appointment_db(appointment_name):
    query = "DELETE FROM Appointment WHERE name = %s "
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (appointment_name, ))
        cursor.close()

CRUD operations for user table implemented.

player()
^^^^^^^^
.. code-block:: python
def get_players_db():
    query = """select * from player
                INNER JOIN team
                ON team.team_id = player.team_id"""
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        return users

def delete_players_db(user_name):
    user_id = get_user_id_with_username(user_name)
    query = "DELETE FROM player WHERE user_id = %s "
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, ))
        cursor.close()

def get_player_with_username(user_name):
    user_id = get_user_id_with_username(user_name)
    query = "select count(*) from player where user_id = %s"
    url = db_url.get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, ))
        exists = cursor.fetchone()
        print("Exists:", exists)
        cursor.close()
        if exists[0] == 1:
            return True
        else:
            return False

def insert_players_db(player, user_name, team_name):
    user_id = get_user_id_with_username(user_name)
    team_id = get_team_id_with_teamname(team_name)
    query = "INSERT INTO PLAYER (name, age, user_id, team_id ) VALUES(%s, %s, %s, %s )"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (player.name, player.age, user_id, team_id))
        cursor.close()
        return True

def update_players_db(player, user_name, team_name):
    user_id = get_user_id_with_username(user_name)
    team_id = get_team_id_with_teamname(team_name)
    query = "UPDATE Player SET name = %s, age = %s, team_id = %s WHERE user_id = %s"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (player.name, player.age, team_id, user_id))
        cursor.close()
        return True

CRUD operations for player table implemented.

team()
^^^^^^^^
.. code-block:: python
def get_teams_db():
    query = "SELECT * FROM Team"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        return users
def insert_teams_db(team):
    query = "INSERT INTO TEAM (name, rating) VALUES(%s, %s)"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (team.name, team.rating))
        cursor.close()
        return True
def update_teams_db(team_name, old_team_name):
    query = "UPDATE Team SET name = %s WHERE name = %s"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (team_name, old_team_name))
        cursor.close()
        return True
def delete_team_db(team_name):
    query = "DELETE FROM Team WHERE name = %s "
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (team_name, ))
        cursor.close()

CRUD operations for team table implemented.

team_extras()
^^^^^^^^
.. code-block:: python
def get_team_id_with_teamname(team_name):
    query = "SELECT team_id FROM Team WHERE name = %s"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (team_name, ))
        team_id = cursor.fetchone()
        cursor.close()
        print("team_id: ", team_id)
        return team_id

def get_team_players_with_team_id(team_id):
    query = "SELECT distinct p.name, p.rating, p.age FROM Team as t, Player as p WHERE p.team_id = %s"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (team_id, ))
        players = cursor.fetchall()
        cursor.close()
        return players

Two extra functions implemented: To get team players using team id, to get team id with team name.


match()
^^^^^^^^
.. code-block:: python
def get_match_db():
    query = "SELECT * FROM Match"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        return users
def insert_match_db(match):
    team1_id = get_team_id_with_teamname(match.team1_name)
    team2_id = get_team_id_with_teamname(match.team2_name)
    query = "INSERT INTO MATCH (team1_id, team2_id) VALUES(%s, %s) RETURNING match_id;"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (team1_id, team2_id, ))
        match_id = cursor.fetchone()
        cursor.close()
        return match_id
def delete_match_db(match):
    query = "DELETE FROM Match WHERE match = %s "
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (match.match_id, ))
        cursor.close()
def update_players_db(player, user_name, team_name):
    user_id = get_user_id_with_username(user_name)
    team_id = get_team_id_with_teamname(team_name)
    query = "UPDATE Player SET name = %s, age = %s, team_id = %s WHERE user_id = %s"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (player.name, player.age, team_id, user_id))
        cursor.close()
        return True

CRUD operations for match table implemented.

stadium()
^^^^^^^^
.. code-block:: python
def get_stadiums_db():
    query = "SELECT * FROM Stadium"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        stads = cursor.fetchall()
        cursor.close()
        return stads
def insert_stadiums_db(stadium):
    query = "INSERT INTO STADIUM (name) VALUES(%s)"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (stadium.name, ))
        cursor.close()
        return True
def update_stadiums_db(stadium_old, stadium_new):
    query = "UPDATE Stadium SET name = %s WHERE name = %s"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (stadium_new, stadium_old))
        cursor.close()
        return True
def delete_stadium_db(stadium_name):
    query = "DELETE FROM stadium WHERE name = %s "
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (stadium_name, ))
        cursor.close()

CRUD operations for stadium table implemented.

get_stad_id_with_stad_name()
^^^^^^^^
.. code-block:: python
def get_stad_id_with_stad_name(stadium_name):
    query = "SELECT stadium_id FROM Stadium WHERE name = %s"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (stadium_name,))
        stad_id = cursor.fetchone()
        cursor.close()
        return stad_id

An extra function implemented: To get stadium id using stadium name.


appointment()
^^^^^^^^
.. code-block:: python
def delete_appointment_db(appointment_name):
    query = "DELETE FROM Appointment WHERE name = %s "
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (appointment_name, ))
        cursor.close()
def get_appointments_db():
    query = """select a.appointment_id, a.name, t1.name, t2.name, s.name, a.start_time, a.end_time, a.date
	            from appointment as a, match as m, stadium as s, team as t1, team as t2
                where (m.match_id = a.match_id AND
			    a.stadium_id = s.stadium_id AND
			    (( m.team1_id = t1.team_id AND m.team2_id = t2.team_id ) ) )"""
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        appointments = cursor.fetchall()
        cursor.close()
        return appointments
def insert_appointments_db(appointment):
    query = "INSERT INTO APPOINTMENT (name, match_id, stadium_id, start_time, end_time, date) VALUES(%s, %s, %s, %s, %s, %s)"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (appointment.name, appointment.match_id, appointment.stadium_id, appointment.start_time, appointment.end_time, appointment.date, ))
        cursor.close()
        return True
def update_appointments_db(appointment_id, username):
    user_id = get_user_id_with_username(username)
    query = """	UPDATE MATCH SET
                 team2_id = (select team_id from player where user_id = %s)
                 WHERE match_id = (select match_id from APPOINTMENT
                 where appointment_id = %s)"""
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, appointment_id, ))
        cursor.close()
        return True

CRUD operations for appointment table implemented.


get_db_url()
^^^^^^^^
.. code-block:: python
def get_db_url():
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    return url

Gets the database url from heroku environment variables.

check_profile_exists()
^^^^^^^^
.. code-block:: python
def check_profile_exists(user_name):
    user_id = db_usr.get_user_id_with_username(user_name)
    query = "SELECT CASE WHEN EXISTS ( SELECT * FROM Player WHERE user_id = %s ) " \
            "THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END"
    url = db_url.get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, ))
        result = cursor.fetchone()
        result = result[0]
        cursor.close()
        if result == "1":
            print("yes, exists:", result)
        else:
            print("not exists:", result)
        return result

Checks if a profile is created for a user, using username.