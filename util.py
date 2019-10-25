from getpass import getpass
import datetime
import re
import random

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

# Asks the user a yes or no question from the message string, takes the input
# from the user and returns a boolean corresponding to the response
# Returns: A boolean either true or false (yes/no)
def promptMessage(message):
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

# Gets the birthdate of the baby and validate it is in the correct format
# Returns: The birthdate of the baby is successfully passed or 'None' if not
def getDate():
	while True:
		# Get the date
		date = input("What is the birthdate in the format"+ 
				 " 'year-month-day', i.e., 1999-05-12\n")
		# Try and except block to test for proper date format
		try:
			datetime.datetime.strptime(date, '%Y-%m-%d')
			return date;
		except ValueError:
			# Check if the user wants to try again
			resume = promptMessage("Incorrect date format, try again?")
			if(resume == False):
				# Returns none if not wanted to try again
				return None


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

# Adds a person to the database
def regPerson(fname, lname, bdate, bplace, address, phone, cursor):
	cursor.execute('''INSERT INTO persons(fname, lname, bdate, bplace, address, phone)
					 VALUES(?,?,?,?,?,?)''', (fname, lname, bdate, bplace,
					 	address, phone))
# Gets the phone number from the agent and verifies it's correctness
def getPhone():
	# Keeps looping until a correct phone number is entered or the agent gives up
	while True:
		# Compile a regex pattern to check for the correctness of an inputted phone number
		pattern = re.compile("(\+[\d]+\s)?\(?[\d]{3}\)?[\-.\s]{1}[\d]{3}[\-.\s]{1}[\d]{4}")
		# Asks the user for the phone number
		phone = input("What is the phone number?\n")
		# Check for a fullmatch of the pattern to the phone number
		if(pattern.fullmatch(phone) is None):
			# Outputs error if the pattern doesn't match
			resume = promptMessage("It seems like there is a typo in your phone number. Try again?")
			# Checks if the agent wants to try inputting the number again
			if resume == False:
				# Return a null string
				return None
		else:
			# Return the correct phone number
			return phone

def handleNotReg(fname, lname, cursor):
	# Display message to the user explaining what's going on
	moreInfo = promptMessage("It looks like " + fname + " "+ lname +" is not registered." +
		"The system will automatically add them to the database, do" +
		" you have any other information?")
	# Initialize variables to None
	bdate = None
	bplace = None
	address = None
	phone = None

	# Check if the agent has more info
	if(moreInfo == True):
		# while True:

		# Check if the agent has various info pertaining to the person
		# Skips the attribute if they don't have the info
		resume = promptMessage("Do you have the birthday?")
		if resume:
			bdate = getDate()
		resume = promptMessage("Do you have the birth place?")
		if resume:
			bplace = input("What is the birthplace?\n")
		resume = promptMessage("Do you have the address?")
		if resume:
			address = input("What is the address?\n")
		resume = promptMessage("Do you have the phone number?")
		if resume:
				phone = getPhone()
			# TODO Verify this info
			# print("Please verify the following information")
			# print("Full name: " + fname + " " + lname)
		# Call regPerson to add the person to the database
		regPerson(fname, lname, bdate, bplace, address, phone, cursor)

	else:
		# Call regPerson to add the person to the database
		regPerson(fname, lname, None, None, None, None, cursor) 

def checkPerson(fname, lname, cursor):
	cursor.execute('''SELECT fname, lname FROM persons''')
	matches = cursor.fetchall()
	for people in matches:
		# print(people[0] + " " + people[1])
		if (people[0].lower() == fname.lower() and
				people[1].lower() == lname.lower()):
			return True
	# print("No match")
	return False
	# print(matches)

def genRegNo(database, cursor):
	# String for the query, used to make the code more modular
	query ="SELECT regno from " + database
	# Execute the query
	nums = cursor.execute(query)
	success = True
	# Keep generating a number until a unique one is created
	while True:
		# Generate a random number
		newReg = random.randint(1, 2000)
		# Check it against existing regNo's
		for num in nums:
			if num[0] == newReg:
				success = False
		# Return the regNo when a unique one is created
		if success == True:
			return newReg

def regBirth(cursor, city):
	# Variables holding whether or not the mother and father are
	# already in the database
	isRegMother = True
	isRegFather = True
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
		return

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

	# Return to menu if unsuccesful
	if(resume == False):
		print("Returning to main menu")
		return

	# Get a valid birthday
	bday = getDate()
	if(bday == None):
		print("Returning to main menu")
		return

	bplace = input("Where was the baby born?")
	# Get the mother's first name
	m_fname, resume = getName("What is the mother's first name? \n")
	
	# Return to menu if unsuccesful
	if(resume == False):
		print("Returning to main menu")
		return
	
	# Get the mother's last name
	m_lname, resume = getName("What is the mother's last name? \n")

	# Return to menu if unsuccesful
	if(resume == False):
		print("Returning to main menu")
		return
	
	isRegistered = checkPerson(m_fname, m_lname, cursor)
	if isRegistered == False:
		isRegMother = False
		handleNotReg(m_fname, m_lname, cursor)

	# Get the father's first name
	f_fname, resume = getName("What is the father's first name? \n")
	# Return to menu if unsuccesful
	if(resume == False):
		print("Returning to main menu")
		return

	# Get the father's last name
	f_lname, resume = getName("What is the father's last name? \n")
	# Return to menu if unsuccesful
	if(resume == False):
		print("Returning to main menu")
		return

	# Check for registration of the father in the database, add him
	# if he is not in the database
	isRegistered = checkPerson(f_fname, f_lname, cursor)
	if isRegistered == False:
		isRegFather = False
		handleNotReg(f_fname, f_lname, cursor)

	# Verify information
	print("Please verify if the following information is correct")
	print("Baby's full name: " + fname + " " + lname)
	print("Baby's gender: " + gender.upper())
	# Checks mother name only if it was previously registered
	if isRegMother:
		print("Mother's name: " + m_fname + " " + m_lname)
	# Checks father name only if it was previously registered
	if isRegFather:
		print("Father's name: " + f_fname + " " + f_lname)
	# Checks with user if all the info was correct
	resume = promptMessage("Is all of this information correct?")

	# Goes back to the main menu if the info is incorrect
	if(resume == False):
		print("Returning to main menu, please try registering again")
		return

	# Get today's date
	regdate = datetime.datetime.date(datetime.datetime.now())
	# Generate a unique regno
	regno = genRegNo("births", cursor)
	# Find the mothers address and phone number
	cursor.execute('''SELECT address, phone FROM persons WHERE fname = ? and
		lname = ?''', (m_fname, m_lname))
	# Fetch the result
	motherInfo = cursor.fetchone()
	# Insert the baby into persons
	cursor.execute('''INSERT into persons VALUES(?,?,?,?,?,?)''',
		(fname, lname, bday, bplace, motherInfo[0], motherInfo[1]))
	# Insert the baby into births
	cursor.execute('''INSERT INTO births VALUES(?,?,?,?,?,?,?,?,?,?)''',
		(regno, fname, lname, regdate, city, gender.upper(), f_fname, f_lname,
				 	m_fname, m_lname))

