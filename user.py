import sqlite3
from getpass import getpass

class User:
    def __init__(self, uid, cursor):
        self.uid = uid
        self.city = None
        self.name = None
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
            self.city = self.cursor.fetchone()[0]
        return self.city

    def getName(self):
        if not self.name:
            self.cursor.execute("SELECT fname FROM users WHERE uid = ?", (self.uid, ))
            self.name = self.cursor.fetchone()[0]
        return self.name

    # Asks the user a yes or no question from the message string, takes the input
    # from the user and returns a boolean corresponding to the response
    # Returns: A boolean either true or false (yes/no)
    def promptMessage(self, message):
        while True:
            # Get the response from the user and convert it to lowercase
            response = input(message + " (y/n)\n").lower()
            if response == 'y':
                return True
            elif response == 'n':
                return False
            else:
                # if y or n is not typed print error and prompt user to try again
                print("Unknown Command")

    # Processes the login of a user
    # Inputs: Cursor - a cursor object connected to the database
    # Returns: 0, 1 or 2 - 0 being login failed, 1 being login succeeded and user
    # is an agent and 2 being login succeeded and user is an officer
    @staticmethod
    def processLogin(cursor):
        username = input("Username: ")

        credentials = (username, )
        cursor.execute("SELECT uid, pwd, utype FROM users WHERE uid LIKE ?", credentials)
        user = cursor.fetchone()

        if not user:
            print("User does not exist")
            return None
        
        password = getpass("Password: ")
        
        if password == user[1]:
            return user
        else:
            print("Wrong password")
            return None