import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url
from db.user.get_user_id import get_user_id_with_username
from db.team.get_team_id import get_team_id_with_teamname


def insert_players_db(player, user_name, team_name):
    user_id = get_user_id_with_username(user_name)
    team_id = get_team_id_with_teamname(team_name)
    query = "INSERT INTO PLAYER (name, age, user_id, team_id ) VALUES(%s, %s, %s, %s )"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (player.name, player.age, user_id, team_id))
        cursor.close()
        return True
