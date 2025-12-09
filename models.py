import sqlite3
from flask import g

DATABASE = '/workspaces/Plant-The-Roses/database.db'

def get_db():
    #If DB already exists
    db = getattr(g, '_database', None)

    #Otherwise, create
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        inCursor = db.cursor()
        table_creation_query = """
        CREATE TABLE GEEK (
            Username VARCHAR(50) NOT NULL,
            Password VARCHAR(50) NOT NULL,
            SavedImg BLOB(50) NOT NULL
            );
        """
        inCursor.execute(table_creation_query)
        print("Table is ready.")

    #return DB
    return db

class Model:
    def attempt():
     return 0