import psycopg2 as dbapi2
import db.get_db_url as db_url

def get_teams_db():
    query = "SELECT * FROM Team"
    url = db_url.get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        return users