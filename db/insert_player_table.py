import psycopg2 as dbapi2
import db.get_db_url as db_url


def insert_players_db(player):
    query = "INSERT INTO PLAYERS (NAME, TEAM_ID, RATING, AVAILABLE) VALUES(%s, %s, %s, %s)"
    url = db_url.get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (player.name, player.team_id, player.rating,
                               player.rating, player.is_available))
        users = cursor.fetchall()
        cursor.close()
        return users
