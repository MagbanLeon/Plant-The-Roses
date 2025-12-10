import sqlite3
from flask import g, session
import os, shutil

class Model:
    def __init__(self):
        # with app.app_context():
            DATABASE = '/workspaces/Plant-The-Roses/database.db'
            self.db = getattr(g, '_database', None)
            self.save_path = '/workspaces/Plant-The-Roses/local'
            if self.db is None:
                self.db = g._database = sqlite3.connect(DATABASE)
                self.cur = self.db.cursor()
                
                #check if DB is empty
                self.cur.execute("SELECT name FROM sqlite_master;")
                check = self.cur.fetchall()
                if not check:   #Create Table if not
                    print("Creating table.")
                    table_creation_query = """
                    CREATE TABLE GEEK (
                        Username VARCHAR(50) NOT NULL,
                        Password VARCHAR(50) NOT NULL,
                        SavedImg BLOB(50)
                        );
                    """
                    self.cur.execute(table_creation_query)
                print("Table is ready.")

    def addAccount(self, newUser, newPass):
        self.cur.execute("INSERT INTO GEEK (Username, Password, SavedImg) VALUES (?, ?, NULL)", (newUser, newPass))
        self.db.commit()
    def verifyAccount(self, checkUser, checkPass):
        self.cur.execute('SELECT * FROM GEEK WHERE Username = ? AND Password = ?', (checkUser, checkPass))
        return self.cur.fetchone()
    def plant(self, username):
        self.cur.execute("SELECT SavedImg FROM GEEK WHERE Username = ?", (username,))
        return self.cur.fetchone()[0]
    def garden(self, data):
        self.unroot() #gets rid of current image file
        with open('static/currentflower.png', 'wb') as file:
            file.write(data)
    def unroot():
        file = 'currentflower.png'
        location = '/workspaces/Plant-The-Roses/static'
        path = os.path.join(location, file)

        os.remove(path)
        print(f"{file} has been removed successfully")
    def addImage(self,file):
        with open('local/'+ os.listdir(self.save_path)[0], 'rb') as file:
                image_data = file.read()
                self.cur.execute("""
                UPDATE GEEK
                SET SavedImg = ?
                WHERE Username = ?;
                """, (image_data, session['username']))
                self.db.commit()
                self.remove(self.save_path)
    def getImage():
        pass
    def remove(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    def close(self):
        self.db = getattr(g, '_database', None)
        if self.db is not None:
            self.db.close()