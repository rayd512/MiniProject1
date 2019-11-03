import datetime
import re
import random

# Adds a person to the database
def regPerson(fname, lname, bdate, bplace, address, phone, cursor):
	cursor.execute('''INSERT INTO persons(fname, lname, bdate, bplace, address, phone)
					 VALUES(?,?,?,?,?,?)''', (fname, lname, bdate, bplace,
					 	address, phone))

# Gets the phone number from the agent and verifies it's correctness
# Returns: The phone number or None if the phone number could not be verified
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

# Handles registering a mother or father who is not in the database
# Inputs: fname - the first name of the person to be added
#		  lname - the last name of the person to be added
#         cursor - a cursor object to the database
def handleNotReg(fname, lname, cursor):
	# Display message to the user explaining what's going on
	moreInfo = promptMessage("- It looks like " + fname + " "+ lname +" is not registered." +
		"The system will automatically add them to the database, do" +
		" you have any other information?")
	# Initialize variables to None
	bdate = None
	bplace = None
	address = None
	phone = None

	# Check if the agent has more info
	if moreInfo:
		# Check if the agent has various info pertaining to the person
		# Skips the attribute if they don't have the info
		if promptMessage("Do you have the birthday?"):
			bdate = getDate()
		if promptMessage("Do you have the birth place?"):
			bplace = input("- What is the birthplace?\n> ")
		if promptMessage("Do you have the address?"):
			address = input("- What is the address?\n> ")
		if promptMessage("Do you have the phone number?"):
			phone = getPhone()
			
	# Call regPerson to add the person to the database
	regPerson(fname, lname, bdate, bplace, address, phone, cursor)

# Generate a unique registration number corresponding to the passed database
# Inputs: table - the table where the unique regNo will go
#         cursor - a cursor object to the database
# Returns: newReg - a unique registration number
def genRegNo(table, cursor):
	# String for the query, used to make the code more modular
	query = "SELECT count(*) from " + table
	cursor.execute(query)
	return cursor.fetchone()[0]
	
# Helper function that checks if the person is already in the database or not
# Inputs: fname - the first name of the person to be added
#		  lname - the last name of the person to be added
#         cursor - a cursor object to the database
# Returns: True or False whether or not the person is in the database
def checkPerson(fname, lname, cursor):
	# Query for the all the first and last names in persons
	credentials = (fname, lname)
	cursor.execute("SELECT count(*) FROM persons where fname LIKE ? and lname LIKE ?", credentials)
	
	# Fetch all the results
	matches = cursor.fetchone()
	if matches[0] == 0:
		return False
	return True

# Asks the user a yes or no question from the message string, takes the input
# from the user and returns a boolean corresponding to the response
# Returns: A boolean either true or false (yes/no)
def promptMessage(message):
	while True:
		# Get the response from the user and convert it to lowercase
		response = input(message + " (y/n)\n> ").lower()
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
		response = input(info + "> ")
		# Check if there is any digits in the inputted string 
		if ( any(char.isdigit() for char in response) or
			response.isspace() or response == ""):

			# Check if the agent wants to try again
			repeat = promptMessage("There seems to be a typo in that name," +
				" would you like to try again?")
			if(repeat == False):
				return None
		else:
			break
	# Return the response and the success token
	return response

# Gets the birthdate of the baby and validate it is in the correct format
# Returns: The birthdate of the baby is successfully passed or 'None' if not
def getDate():
	while True:
		# Get the date
		date = input("- What is the birthdate in the format"+ 
				 " 'year-month-day', i.e., 1999-05-12\n> ")
		# Try and except block to test for proper date format
		try:
			datetime.datetime.strptime(date, '%Y-%m-%d')
			return date
		except ValueError:
			# Check if the user wants to try again
			resume = promptMessage("Incorrect date format, try again?")
			if(resume == False):
				# Returns none if not wanted to try again
				return None

def getPaymentAmount():
	while True:
		pass
		amount = input("What is the paymount amount? i.e '9', with no $ sign")

		if not amount.isdigit():
			resume = promptMessage("Invalid input, would you like to try again?")

			if not resume:
				return None