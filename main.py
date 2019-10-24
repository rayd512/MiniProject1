import sqlite3
import sys
import util
import officer
import agent

def main():
	# Check that a command line argument for the database path was passed
	if(len(sys.argv) != 2):
		# Output an error message
		print("Error: Path of database expected")
	# Assign the path to a variable
	database_path = sys.argv[1]
	# Create a connection with the database
	connection = sqlite3.connect(database_path)
	# Create a cursor object for the database
	cursor = connection.cursor()
	# Calls processLogin function to check if the user
	# successfully logs in
	loginType, uid = util.processLogin(cursor)

	# Perform the action corresponding to the login type
	if loginType == 0:
		return
	elif loginType == 1:
		agent.agentActions(uid, cursor)
		# print("Agent")
	elif loginType == 2:
		officer.officerActions()
		print("Officer")



if __name__ == '__main__':
	main()