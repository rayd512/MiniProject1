import sqlite3

class User:
    def __init__(self, uid, cursor):
        self.uid = uid
        self.city = None
        self.cursor = cursor
        self.loggedIn = True
        self.toExit = False
    
    def logout(self):
        self.loggedIn = False
    
    def exit(self):
        self.toExit = True

    def isLoggedIn(self):
        return self.loggedIn

    def isExit(self):
        return self.toExit

    def getCity(self):
        if not self.city:
            self.cursor.execute("SELECT city FROM users WHERE uid = ?", (self.uid, ))
            self.city = self.cursor.fetchall()
        return self.city
        
    # def query(self, statement, args):
    #     if not self.city:
    #         self.cursor.execute(statement, args)