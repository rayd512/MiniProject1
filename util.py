from getpass import getpass

# Processes the login of a user
# Inputs: Cursor - a cursor object connected to the database
# Returns: 0, 1 or 2 - 0 being login failed, 1 being login succeeded and user
# is an agent and 2 being login succeeded and user is an officer
def processLogin(cursor):
	# Boolean holding whether the user wants to
	# try to login again after failed attempts
	getCredentials = False
	# Boolean holding if the login was a success
	loginSuccess = False
	while(getCredentials == False):
		# Get the user's usernames
		username = input("Username: ")
		# Execute an sql command
		cursor.execute('''SELECT uid FROM users''')
		# Return all the results from the query
		all_users = cursor.fetchall()

		# Instantiate a boolean to see if the username is found
		found_user = False
		# Parse the results of the query
		parsed_users = [all_users[0] for all_users in all_users]
		# Loop through all the users
		for users in parsed_users:
			# print(users)
			if(users == username):
				found_user = True
				break

		if(found_user != True):
			# Output error 
			print("Username not found, please check and try again")
			# Check if user wants to try again
			response = input("Try again? (y/n) ").lower()
			if(response != "y"):
				loginSuccess = False
				getCredentials = True
			else:
				continue

		# Skips password if user didn't want to try again
		if (getCredentials != True):
			# Get the password from the user, getpass hides the password
			pwd = getpass()

			# Get stored password corresponding to the username
			cursor.execute('''SELECT pwd FROM users where uid = ?''', (username,))
			passwords = cursor.fetchall()
			
			# Parse the password
			parsed_pwd = [passwords[0] for passwords in passwords]
			# print(parsed_pwd[0]) ---> DEBUGGING
			# There should only be one password, report error if not
			if(len(parsed_pwd) > 1):
				print("Internal Error")
				return 0

			if(parsed_pwd[0] != pwd):
				# Checks if user wants to try again
				print("Incorrect password, please check and try again")
				response = input("Try again? (y/n) ")
				if(response != "y"):
					loginSuccess = False
			else:
				# Login was a success
				loginSuccess = True
				getCredentials = True

	# If the login was a success
	if loginSuccess == True:
		# Find if the user that logged in is an agent or officer
		cursor.execute('''SELECT utype FROM users where uid = ?''', (username,))
		utypes = cursor.fetchall()
		# Parse the result
		parsed_utype = [utypes[0] for utypes in utypes]
		# return the appropriate value
		if parsed_utype[0] == "a":
			return 1
		elif parsed_utype[0] == 'o':
			return 2
	else:
		return 0;

def promptMessage():
	response = input("Would you like to perform another task? (y/n)")
	while True:
		if response == 'y':
			return True
		elif response == 'n':
			return False
		else:
			print("Unknown Command")

def dispAgentActions():
	print("Type 'regBirth' to register a birth")
	print("Type 'regMarriage' to register a marriage")
	print("Type 'renewVreg' to renew a vehicle registration")
	print("Type 'processBOS' to process a bill of sale")
	print("Type 'procPayment' to process a payment")
	print("Type 'getAbstract' to get a driver abstract")
	print("Type 'logout' to logout the program")
	print("Type 'exit' to exit the program")