import psycopg2 as dbapi2
from db.utils.get_db_url import get_db_url
from db.user.get_user_id import get_user_id_with_username

def delete_match_db(match):
    query = "DELETE FROM Match WHERE match = %s "
    url = get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (match.match_id, ))
        cursor.close()

