import os
import sys
import psycopg2 as dbapi2


def insert_players_db(player):
    query = "INSERT INTO PLAYERS (NAME, GENRE, DURATION_IN_SECONDS, SINGER, YEAR) VALUES(%s, %s, %s, %s, %s)"
    url = insert_players_db()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (player.name, player.team_id, player.rating,
                               player.rating, player.is_available))
        users = cursor.fetchall()
        cursor.close()
        return users
