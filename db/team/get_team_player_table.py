import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url


def get_team_players_with_team_id(team_name):
    query = "SELECT distinct p.name FROM Team as t, Player as p" \
            "WHERE p.team_id = %s"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (team_name, ))
        team_id = cursor.fetchone()
        cursor.close()
        print("team_id: ", team_id)
        return team_id