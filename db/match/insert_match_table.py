import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url
from db.user.get_user_id import get_user_id_with_username
from db.team.get_team_id import get_team_id_with_teamname


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
