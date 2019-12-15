import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url


def update_users_db(username, password):
    query = "UPDATE Users SET password = %s WHERE name = %s"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (password, username, ))
        cursor.close()

