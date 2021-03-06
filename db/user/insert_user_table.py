import psycopg2 as dbapi2
import db.utils.get_db_url as db_url


def insert_users_db(user):
    query = "INSERT INTO USERS (name, password) VALUES(%s, %s)"
    url = db_url.get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (user.name, user.password))
        cursor.close()
