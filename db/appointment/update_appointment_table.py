import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url
from db.user.get_user_id import get_user_id_with_username


def update_appointments_db(appointment_id, username):
    user_id = get_user_id_with_username(username)
    query = """	UPDATE MATCH SET
                 team2_id = (select team_id from player where user_id = %s)
                 WHERE match_id = (select match_id from APPOINTMENT
                 where appointment_id = %s)"""
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, appointment_id, ))
        cursor.close()
        return True
