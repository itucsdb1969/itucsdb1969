import psycopg2 as dbapi2
import db.get_db_url as db_url
import db.get_user_id as db_usr
import db.get_team_id as db_team


def insert_players_db(user_name):
    user_id = db_usr.get_user_id_with_username(user_name)
    query = "DELETE FROM player WHERE user_id = % "
    url = db_url.get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, ))
        cursor.close()

