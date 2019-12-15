import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url


def get_stadiums_db():
    query = "SELECT * FROM Stadium"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        stads = cursor.fetchall()
        cursor.close()
        return stads
