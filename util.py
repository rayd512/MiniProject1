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
				return 0, None

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
			return 1, username
		elif parsed_utype[0] == 'o':
			return 2, username
	else:
		# Return that a login was not succesful
		return 0, None;

def promptMessage(message):
	while True:
		response = input(message + " (y/n)\n").lower()
		if response == 'y':
			return True
		elif response == 'n':
			return False
		else:
			print("Unknown Command")

# Prompts the user to input a name based on the info string. The function
# will then check if the name has any numbers in it, it will ask the agent
# if he or her wants to try inputting that name again
# Inputs: info - a string that holds what the program is going to ask the 
#				 agent to input
# Returns: tuple - first being the name inputted and the second whether or
# 				   or not the agent was able to input a proper name
def getName(info):
	# Keep asking for info if the agent wants to try again
	while True:
		# Take in the response from the agent
		response = input(info)
		# Check if there is any digits in the inputted string 
		if(any(char.isdigit() for char in response)):
			# Check if the agent wants to try again
			repeat = promptMessage("There seems to be a typo in that name," +
				" would you like to try again?")
			# Break if the agent doesn't want to try again
			if(repeat == False):
				return None, False
		else:
			# Succesful input, break
			break
	# Return the response and the success token
	return response, True

def checkDate():
	pass

# Prints to the screen the commands available to an agent
def dispAgentActions():
	print("Type 'regBirth' to register a birth")
	print("Type 'regMarriage' to register a marriage")
	print("Type 'renewVreg' to renew a vehicle registration")
	print("Type 'processBOS' to process a bill of sale")
	print("Type 'procPayment' to process a payment")
	print("Type 'getAbstract' to get a driver abstract")
	print("Type 'logout' to logout the program")
	print("Type 'exit' to exit the program")

def regBirth():
	# Prompt information on to the screen
	print("Registering a birth...")
	print("Please ensure you have the baby's first name, last name, " +
		"birthplace, father's first name, father's last name, mother's" + 
		" first name and mother's last name")
	# Check if the Agent is ready to input 
	ready = promptMessage("Do you have all this info ready?")

	# Return to the main menu if the agent is not ready
	if(ready == False):
		print("Returning to main menu")

	# Call get name to get the babies first name with basic error checking
	fname, resume = getName("What is the baby's first name?\n")

	# If the agent made a typo entering the name and doesn't want to 
	# continue, the program will go back to the main menu
	if(resume == False):
		print("Returning to main menu")
		return

	# Get the last name of the baby
	lname, resume = getName("What is the baby's last name?\n")
	if(resume == False):
		print("Returning to main menu")
		return

	# Get the gender of the baby, will check if something other than
	# 'm' or 'f' is entered and will ask the user if it wants to try again
	while True:
		gender = input("What is the baby's gender? (M/F)\n").lower()
		if(gender == "m" or gender == "f"):
			resume = True
			break
		else:
			resume = promptMessage("Unknown gender, try again?")
			if resume == False:
				break

	if(resume == False):
		print("Returning to main menu")
		return

	bday = input("What is the birthdate of the baby in the format"+ 
				" 'year-month-day', i.e., 1999-05-12\n" )
	
	m_fname, resume = getName("What is the mother's first name? \n")
	
	if(resume == False):
		print("Returning to main menu")
		return
	
	m_lname, resume = getName("What is the mother's last name? \n")
	
	if(resume == False):
		print("Returning to main menu")
		return
	
	f_fname, resume = getName("What is the father's first name? \n")
	if(resume == False):
		print("Returning to main menu")
		return
	f_lname, resume = getName("What is the father's last name? \n")
	if(resume == False):
		print("Returning to main menu")
		return
	# birthInfo = input("Please input the birth info in a comma " +
	# 	"seperated list in the following format: First name, Last Name" +
	# 	"birthplace, Father's first name, Father's last name, Mother's" + 
	# 	" first name, Mother's last name\n" + "For example: Micheal, Fox, " +
	# 	" Edmonton, AB")
