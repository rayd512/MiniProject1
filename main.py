import sqlite3
import sys

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

	
	cursor.execute("Select * from users")
	user = cursor.fetchone()
	print(user)
	print(database_path)
	


if __name__ == '__main__':
	main()