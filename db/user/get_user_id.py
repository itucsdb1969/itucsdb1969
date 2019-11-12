import psycopg2 as dbapi2
import db.utils.get_db_url as db_url


def get_user_id_with_username(user_name):
    query = "SELECT user_id FROM Users WHERE name = %s"
    url = db_url.get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (user_name, ))
        user_id = cursor.fetchone()
        cursor.close()
        return user_id
