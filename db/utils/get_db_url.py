import os
import sys


def get_db_url():
    url = os.getenv("DATABASE_URL")
    # url = "dbname='postgres' user='postgres' host='localhost' password='postgres'"
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    return url