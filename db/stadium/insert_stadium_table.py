import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url


def insert_stadiums_db(stadium):
    query = "INSERT INTO STADIUM (name) VALUES(%s)"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (stadium.name, ))
        cursor.close()
        return True
