import psycopg2 as dbapi2
import db.get_db_url as db_url
import db.get_user_id as db_usr
import db.get_team_id as db_team


def update_players_db(player, user_name, team_name):
    user_id = db_usr.get_user_id_with_username(user_name)
    team_id = db_team.get_team_id_with_teamname(team_name)
    query = "UPDATE Player SET name = %s, age = %s, team_id = %s WHERE user_id = %s"
    url = db_url.get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (player.name, player.age, team_id, user_id))
        cursor.close()
        return True
