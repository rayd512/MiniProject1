import sqlite3
import os
import sys
import util
from officer.officer import Officer
from agent.agent import Agent

def main():
	# Check that a command line argument for the database path was passed
	if(len(sys.argv) != 2):
		print("Error: Path of database expected")
		sys.exit(0)

	# Assign the path to a variable
	database_path = sys.argv[1]
	
	if (os.path.isfile(database_path)):
		connection = sqlite3.connect(database_path)
	else:
		print("Error: Database does not exist")
		sys.exit(0)
	
	cursor = connection.cursor()

	while True:
		userCreds = util.processLogin(cursor)

		if not userCreds:
			continue

		# uid is first element in the userCreds list
		if userCreds[2] == 'a':
			user = Agent(userCreds[0], cursor)
		else:
			user = Officer(userCreds[0], cursor)
		

		while True:
			if not user.isLoggedIn():
				break

			if user.isExit():
				return
			
			user.processJobs()
			
		# loginType, uid = util.processLogin(cursor)

		# if (loginType == 1):
		# 	person = Agent()
		# else:
		# 	person = Officer()

		# while True:
		# 	if not person.loggedIn:
		# 		break

		# Commit any changes made to the database
		# connection.commit()


if __name__ == '__main__':
	main()