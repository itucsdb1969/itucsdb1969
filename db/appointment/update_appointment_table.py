import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url



def update_appointments_db(appointment, appointment_name):
    query = "UPDATE APPOINTMENT SET name = %s  match_id= %s stadium_id = %s start_time = %s end_time = %s WHERE name = %s"
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (appointment.name, appointment.match_id, appointment.stadium_id. appointment.start_time, appointment.end_time, appointment_name))
        cursor.close()
        return True
