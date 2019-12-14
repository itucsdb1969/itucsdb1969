import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url
from db.user.get_user_id import get_user_id_with_username
from db.team.get_team_id import get_team_id_with_teamname
"""CREATE TABLE IF NOT EXISTS Match(
            match_id SERIAL NOT NULL PRIMARY KEY,
            team1_id INTEGER,
            team2_id INTEGER,
            FOREIGN KEY (team1_id) REFERENCES Team(team_id) ON DELETE CASCADE ON UPDATE CASCADE ,
            FOREIGN KEY (team2_id) REFERENCES Team(team_id) ON DELETE CASCADE ON UPDATE CASCADE
        )"""


def insert_match_db(match):
    team1_id = get_team_id_with_teamname(match.team1_name)
    team2_id = get_team_id_with_teamname(match.team2_name)
    query = "INSERT INTO MATCH (team1_id, team2_id) VALUES(%s, %s) RETURNING match_id;"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        match_id = cursor.execute(query, (team1_id, team2_id))
        cursor.close()
        return match_id
