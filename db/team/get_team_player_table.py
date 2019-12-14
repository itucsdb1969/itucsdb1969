import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url


def get_team_players_with_team_id(team_id):
    query = "SELECT distinct p.name, p.rating, p.age FROM Team as t, Player as p" \
            "WHERE p.team_id = %s"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (team_id, ))
        players = cursor.fetchone()
        cursor.close()
        return players