import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url
from db.user.get_user_id import get_user_id_with_username
from db.team.get_team_id import get_team_id_with_teamname
"""
CREATE TABLE IF NOT EXISTS Player(
            player_id SERIAL NOT NULL PRIMARY KEY,
            team_id INTEGER,
            user_id INTEGER,
            name VARCHAR (50) NOT NULL,
            rating NUMERIC(3,2),
            age INTEGER,
            FOREIGN KEY (team_id) REFERENCES Team(team_id) ON DELETE CASCADE ON UPDATE CASCADE
            FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE ON UPDATE CASCADE
        )
"""


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
