import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url

def get_stad_id_with_stad_name(stadium_name):
    query = "SELECT stadium_id FROM Stadium WHERE name = %s"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (stadium_name,))
        stad_id = cursor.fetchone()
        cursor.close()
        return stad_id
