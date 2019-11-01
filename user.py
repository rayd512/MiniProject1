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
            self.city = self.cursor.fetchone()[0]
        return self.city


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


    # def query(self, statement, args):
    #     if not self.city:
    #         self.cursor.execute(statement, args)