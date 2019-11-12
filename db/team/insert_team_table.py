import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url


def insert_teams_db(team):
    query = "INSERT INTO TEAM (name, rating) VALUES(%s, %s)"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (team.name, team.rating))
        cursor.close()
        return True
