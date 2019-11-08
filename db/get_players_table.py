import os
import sys
import psycopg2 as dbapi2


def get_players_db():
    query = "SELECT * FROM Players"
    url = get_players_db()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        return users
