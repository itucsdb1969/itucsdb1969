import psycopg2 as dbapi2
import db.utils.get_db_url as db_url


def get_user_pw_with_username(user_name):
    query = "SELECT password FROM Users WHERE name = %s"
    url = db_url.get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (user_name, ))
        password = cursor.fetchone()
        print(password)
        cursor.close()
        return password
