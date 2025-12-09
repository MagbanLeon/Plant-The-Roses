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
        
        #check if DB is empty
        inCursor.execute("SELECT name FROM sqlite_master;")
        check = inCursor.fetchall()
        if not check:   #Create Table if not
            print("Creating table.")
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
    def getAccount():
        return 0
    def addAccount(newUser, newPass):
        c.execute("INSERT INTO GEEK (Username, Password) VALUES (%s, %s)", (newUser, newPass))
        return 0
    def verifyAccount(checkUser, checkPass):
        return 0
    def addImage(imageURL):
        return 0
    def getImages():
        return 0