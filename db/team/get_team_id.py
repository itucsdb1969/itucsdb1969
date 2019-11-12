import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url


def get_team_id_with_teamname(team_name):
    query = "SELECT team_id FROM Team WHERE name = %s"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (team_name, ))
        team_id = cursor.fetchone()
        cursor.close()
        print("team_id: ", team_id)
        return team_id
