import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url
"""
class Appointment:
    def __init__(self, name, match_id, stadium_id, start_time, end_time):
        self.name = name
        self.match_id = match_id
        self.stadium_id = stadium_id
        self.start_time = start_time
        self.end_time = end_time

"""


def insert_appointments_db(appointment):
    query = "INSERT INTO APPOINTMENT (name, match_id, stadium_id, start_time, end_time) VALUES(%s, %s, %s, %s, %s)"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (appointment.name, appointment.match_id, appointment.stadium_id, appointment.start_time, appointment.end_time, ))
        cursor.close()
        return True


