import psycopg2 as dbapi2
import db.utils.get_db_url as db_url
from db.user.get_user_id import get_user_id_with_username

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
