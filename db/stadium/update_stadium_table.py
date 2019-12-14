import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url
from db.user.get_user_id import get_user_id_with_username
from db.team.get_team_id import get_team_id_with_teamname


def update_players_db(stadium, stadium_new):
    query = "UPDATE Stadium SET name = %s WHERE name = %s"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (stadium.name, stadium_new, ))
        cursor.close()
        return True
