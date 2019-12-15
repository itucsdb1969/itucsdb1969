import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url

def update_stadiums_db(stadium, stadium_new):
    query = "UPDATE Stadium SET name = %s WHERE name = %s"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (stadium_new, stadium.name))
        cursor.close()
        return True
