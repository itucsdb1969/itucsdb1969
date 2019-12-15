import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url


def get_appointments_db():
    query = """select a.appointment_id, a.name, t1.name, t2.name, s.name, a.start_time, a.end_time
	            from appointment as a, match as m, stadium as s, team as t1, team as t2
                where (m.match_id = a.match_id AND
			    a.stadium_id = s.stadium_id AND
			    (( m.team1_id = t1.team_id AND m.team2_id = t2.team_id ) ) )"""
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        appointments = cursor.fetchall()
        cursor.close()
        return appointments