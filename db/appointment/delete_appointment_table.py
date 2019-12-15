import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url


def delete_appointment_db(appointment_name):
    query = "DELETE FROM Appointment WHERE name = %s "
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (appointment_name, ))
        cursor.close()

