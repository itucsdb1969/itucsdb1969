import psycopg2 as dbapi2
import db.get_user_id as db_usr
import db.get_db_url as db_url


def check_profile_exists(user_name):
    user_id = db_usr.get_user_id_with_username(user_name)
    query = "SELECT CASE WHEN EXISTS ( SELECT * FROM Player WHERE user_id = %s ) " \
            "THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END"
    url = db_url.get_db_url()
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, ))
        result = cursor.fetchone()
        cursor.close()
        if result == 1:
            print("yes, exists:", result)
        else:
            print("not exists:", result)
        return result
