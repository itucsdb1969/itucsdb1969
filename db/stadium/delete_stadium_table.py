import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url


def delete_stadium_db(stadium_name):
    query = "DELETE FROM stadium WHERE name = %s "
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (stadium_name, ))
        cursor.close()
