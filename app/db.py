import sqlite3


def initDb(dbName):
    conn = sqlite3.connect(dbName)

    # Do some setup
    # cur = conn.cursor()
    # cur.executescript('''
    # DROP TABLE IF EXISTS Object;
    # DROP TABLE IF EXISTS Approach;
    #
    # CREATE TABLE Object (
    #     id     INTEGER NOT NULL PRIMARY KEY UNIQUE,
    #     name   TEXT UNIQUE,
    #     hazardous INTEGER,
    #     diameter_min REAL,
    #     diameter_max REAL
    # );
    #
    # CREATE TABLE Approach (
    #     id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    #     date INTEGER,
    #     miss REAL,
    #     object_id INTEGER NOT NULL,
    #     FOREIGN KEY(object_id) REFERENCES Object(id)
    # );
    # ''')

    # print("Database initialized")

    return(conn)

def insertObj(cur, id, name, hazardous, diameter_min, diameter_max):
    return cur.execute(
        '''INSERT OR IGNORE INTO Object (id, name, hazardous, diameter_min, diameter_max) VALUES ( ?, ?, ?, ?, ? )''',
        ( id, name, hazardous, diameter_min, diameter_max )
    )

def insertApproach(cur, date, miss, object_id):
    return cur.execute(
        '''INSERT OR IGNORE INTO Approach (date, miss, object_id) VALUES ( ?, ?, ? )''',
        ( date, miss, object_id )
    )

def getApproaches(cur):
    return cur.execute('SELECT Object.name, Approach.date, Approach.miss FROM Approach JOIN Object ON Approach.object_id = Object.id ')
