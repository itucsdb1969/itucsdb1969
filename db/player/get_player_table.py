import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url


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
