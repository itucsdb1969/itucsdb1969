import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url
from db.user.get_user_id import get_user_id_with_username
from db.team.get_team_id import get_team_id_with_teamname


def update_players_db(player, user_name, team_name):
    user_id = get_user_id_with_username(user_name)
    team_id = get_team_id_with_teamname(team_name)
    query = "UPDATE Player SET name = %s, age = %s, team_id = %s WHERE user_id = %s"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (player.name, player.age, team_id, user_id))
        cursor.close()
        return True
