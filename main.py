import sqlite3
import os
import sys
from user import User
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
	
	# Instantiate a cursor
	cursor = connection.cursor()

	# Infinite loop while the program is running
	while True:
		# Process the login of the user
		userCreds = User.processLogin(cursor)

		# If login fails, go back to login processing
		if not userCreds:
			continue

		# uid is first element in the userCreds list
		if userCreds[2] == 'a':
			# Instantiate an agent object
			user = Agent(userCreds[0], cursor, connection)
		else:
			# Instantiate an agent object
			user = Officer(userCreds[0], cursor, connection)
		
		# Loop through actions of agent or officer
		while True:
			# Check if the user logged out
			if not user.isLoggedIn():
				break

			# Check if the user exit
			if user.isExit():
				# Commit changes to the database
				connection.commit()
				return
			# Check what job the user wants to do.
			user.processJobs()
			# Commit any changes made to the database
			connection.commit()


if __name__ == '__main__':
	main()