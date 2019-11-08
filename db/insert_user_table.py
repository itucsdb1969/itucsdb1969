import psycopg2 as dbapi2
import db.get_db_url as db_url


def insert_users_db(user):
    query = "INSERT INTO USERS (user_id, name, password, is_active, is_admin) VALUES(%s, %s, %s, %s, %s)"
    url = db_url.get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (user.id, user.name, user.password,
                               user.is_active, user.is_admin))
        users = cursor.fetchall()
        cursor.close()
        return users
