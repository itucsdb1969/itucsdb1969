import os
import sys
import psycopg2 as dbapi2

DROP_STATEMENTS = [
    "DROP TABLE IF EXISTS Users cascade",
    "DROP TABLE IF EXISTS Player cascade",
    "DROP TABLE IF EXISTS Team cascade",
    "DROP TABLE IF EXISTS Match cascade",
    "DROP TABLE IF EXISTS Stadium cascade",
    "DROP TABLE IF EXISTS Appointment cascade"
]

INIT_STATEMENTS = [

    """CREATE TABLE IF NOT EXISTS Users(
            user_id SERIAL NOT NULL PRIMARY KEY,
            name VARCHAR(20) UNIQUE NOT NULL,
            password VARCHAR(64),
            is_active BOOLEAN DEFAULT TRUE,
            is_admin BOOLEAN DEFAULT FALSE
        )""",
    
    """
    CREATE TABLE IF NOT EXISTS Team(
            team_id SERIAL NOT NULL PRIMARY KEY,
            name VARCHAR (50) UNIQUE NOT NULL,
            rating NUMERIC(3,2),
            is_available BOOLEAN DEFAULT TRUE
        )""",
    
    """CREATE TABLE IF NOT EXISTS Player(
            player_id SERIAL NOT NULL PRIMARY KEY,
            team_id INTEGER,
            user_id INTEGER,
            name VARCHAR (50) NOT NULL,
            rating NUMERIC(3,2),
            age INTEGER,
            FOREIGN KEY (team_id) REFERENCES Team(team_id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
        )""",
    """
    
    CREATE TABLE IF NOT EXISTS Match(
            match_id SERIAL NOT NULL PRIMARY KEY,
            team1_id INTEGER,
            team2_id INTEGER,
            FOREIGN KEY (team1_id) REFERENCES Team(team_id) ON DELETE CASCADE ON UPDATE CASCADE ,
            FOREIGN KEY (team2_id) REFERENCES Team(team_id) ON DELETE CASCADE ON UPDATE CASCADE
        )""",

    """CREATE TABLE IF NOT EXISTS Stadium(
            stadium_id SERIAL NOT NULL PRIMARY KEY,
            name VARCHAR (50) UNIQUE NOT NULL
        )""",

    """CREATE TABLE IF NOT EXISTS Appointment(
            appointment_id SERIAL NOT NULL PRIMARY KEY,
            name VARCHAR (50) NOT NULL,
            match_id INTEGER NOT NULL,
            stadium_id INTEGER,
            start_time VARCHAR (5) NOT NULL ,
            end_time VARCHAR (5) NOT NULL ,
            FOREIGN KEY (match_id) REFERENCES Match(match_id) ON DELETE RESTRICT ON UPDATE CASCADE ,
            FOREIGN KEY (stadium_id) REFERENCES Stadium(stadium_id) ON DELETE RESTRICT ON UPDATE CASCADE   
        )""",
    """INSERT INTO TEAM (NAME, RATING) VALUES('Galatasaray', '5.0');""",
    """INSERT INTO TEAM (NAME, RATING) VALUES('Fenerbahce', '4.5');""",
    """INSERT INTO TEAM (NAME, RATING) VALUES('Besiktas', '4.2');""",
    """INSERT INTO TEAM (NAME, RATING) VALUES('Trabzonspor', '4.0');""",
    """INSERT INTO TEAM (NAME, RATING) VALUES('Konyaspor', '3.5');""",
    """INSERT INTO TEAM (NAME, RATING) VALUES('Kayserispor', '2.5');""",
    """INSERT INTO TEAM (NAME, RATING) VALUES('Malatyaspor', '1.5');""",
    """INSERT INTO TEAM (NAME, RATING) VALUES('Bursaspor', '0.5');""",
    """INSERT INTO STADIUM (NAME) VALUES ('Ali Sami Yen Spor Kompleksi TT Arena');""",
    """INSERT INTO STADIUM (NAME) VALUES ('Sukru Saracoglu Stadyumu');"""
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in DROP_STATEMENTS:
            cursor.execute(statement)
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    #url = "dbname='itucsdb1969' user='postgres' host='localhost' password='123456'"
    #initialize(url)
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
