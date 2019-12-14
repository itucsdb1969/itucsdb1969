import os
import sys


def get_db_url():
    url = os.getenv("DATABASE_URL")
    # url = "dbname='itucsdb1969' user='postgres' host='localhost' password='postgres'"
    #url = "dbname='postgres' user='postgres' host='localhost' password='123456'"
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    return url
