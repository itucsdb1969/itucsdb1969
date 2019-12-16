import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url


def update_teams_db(team_name, old_team_name):
    query = "UPDATE Team SET name = %s WHERE name = %s"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (team_name, old_team_name))
        cursor.close()
        return True
