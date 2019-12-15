import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url


def delete_users_db(username):
    query = "DELETE FROM Users WHERE name = %s "
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (username, ))
        cursor.close()

