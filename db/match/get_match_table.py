import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url


def get_match_db():
    query = "SELECT * FROM Match"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        return users
