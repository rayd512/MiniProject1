from getpass import getpass
import datetime
import re
import random
from dateutil.relativedelta import relativedelta

# Processes the login of a user
# Inputs: Cursor - a cursor object connected to the database
# Returns: 0, 1 or 2 - 0 being login failed, 1 being login succeeded and user
# is an agent and 2 being login succeeded and user is an officer
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
		date = input("What is the birthdate in the format"+ 
				 " 'year-month-day', i.e., 1999-05-12\n")
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

# Helper function that checks if the person is already in the database or not
# Inputs: fname - the first name of the person to be added
#		  lname - the last name of the person to be added
#         cursor - a cursor object to the database
# Returns: True or False whether or not the person is in the database
def checkPerson(fname, lname, cursor):
	# Query for the all the first and last names in persons
	cursor.execute('''SELECT fname, lname FROM persons''')
	# Fetch all the results
	matches = cursor.fetchall()
	# Loop through all the results
	for people in matches:
		# Check for a match
		if (people[0].lower() == fname.lower() and
				people[1].lower() == lname.lower()):
			return True
	# Return false if there was no match
	return False

# Generate a unique registration number corresponding to the passed database
# Inputs: table - the table where the unique regNo will go
#         cursor - a cursor object to the database
# Returns: newReg - a unique registration number
def genRegNo(table, cursor):
	# String for the query, used to make the code more modular
	query ="SELECT regno from " + table
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


# Renews a vehicle registration
# Inputs: cursor - an instance of the cursor object connected to the database
def renewVReg(cursor):
	# Print info and check if agent has all the required information
	print("Renewing a vehicle registration...")
	print("You will need the registration no.")
	resume = promptMessage("Do you have this info?")
	# Abort if agent doesn't have the required info
	if resume == False:
		print("Returning to main menu")
		return

	# Get the registration number and check that it is only made up of numbers
	while True:
		regNo = input("What is the vehicle registration number?\n")
		if regNo.isdigit() == False:
			resume = promptMessage("Vehicle registration number can only" + 
				" digits. Would you like to try again?")
			if resume == False:
				print("Returning to main menu")
				return
		else:
			break

	# Find the expiry date of the registration
	cursor.execute('''SELECT expiry FROM registrations WHERE regno = ?''', (regNo,))
	# Fetch the query result
	regExpr = cursor.fetchone()
	# Convert expiry to a datetime object
	currentExpr = datetime.datetime.strptime(regExpr[0], '%Y-%m-%d')
	# Get today's date as date time
	dateToday = datetime.datetime.now()
	# Check if the expiry has already expired
	if currentExpr <= dateToday:
		# Add one year to today's date
		newExpr = dateToday + relativedelta(years=+1)
	else:
		# Add one year to the currentexpiry date
		newExpr = currentExpr + relativedelta(years=+1)

	# Update the expiry in the database 
	cursor.execute('''UPDATE registrations SET expiry = ? WHERE regno = ?''',
		(newExpr, regNo))

# Processes a bill of sale
# Inputs: cursor - an instance of the cursor object connected to the database
def processBOS(cursor):
	# Print info and check if agent has all the required information
	print("Processing a bill of sale...")
	print("You will need the vin, name of the current owner, " + 
		"name of the new owner, and a plate number for the new" +
		" registration")
	resume = promptMessage("Do you have all this information?")
	# Abort if agent doesn't have the required info
	if resume == False:
		print("Returning to main menu")
		return

	# Get the vin of the car being sold
	vin = input("What is the VIN of the vehicle\n")

	# Get the buyer a seller's name, abort if agent could not properly
	# fill out any of the names
	seller_fname = getName("What is the seller's first name?\n")
	if not seller_fname:
		print("Returning to main menu")
		return

	seller_lname = getName("What is the seller's last name?\n")
	if not seller_lname:
		print("Returning to main menu")
		return

	buyer_fname, resume = getName("What is the buyer's first name?\n")
	if(resume == False):
		print("Returning to main menu")
		return

	buyer_lname, resume = getName("What is the buyer's last name?\n")
	if not buyer_lname:
		print("Returning to main menu")
		return

	# Get the new plate number
	plate_num = input("What is the new plate number?\n")

	# Get the first name and last name attached to the car
	cursor.execute('''SELECT fname, lname, expiry FROM registrations WHERE vin = ?''',
		(vin,))

	# Fetch the info
	ownerInfo = cursor.fetchone()

	# Check if the seller IS the owner of the vehicle, output message if not
	if (ownerInfo[0].lower() != seller_fname.lower()
			or ownerInfo[1].lower() != seller_lname.lower()):
		print("The owner of this car is not the same as the seller. " +
			"This transfer cannot be made.")
		print("Returning to main menu")
		return

	# Confirm the entered information with the agent
	print("Please confirm the following information")
	print("Seller's name: " + seller_fname + " " + seller_lname)
	print("Buyer's name: " + buyer_fname + " " + buyer_lname)
	print("VIN: " + vin)
	print("New plate number: " + plate_num)
	resume = promptMessage("Is all this information correct?")
	# Abort if there is incorrect information
	if resume == False:
		print("Returning to main menu")
		return


	# Get today's date as date time
	dateToday = datetime.date.today()
	# Add one year from today's date
	newExpr = dateToday + relativedelta(years=+1)
	# Generate a registration number
	regNo = genRegNo("registrations", cursor)
	# Update the current record with all the new info
	cursor.execute('''UPDATE registrations SET regno = ?, 
		regdate = ?, expiry = ?, plate = ?, fname = ?, lname = ? WHERE
		vin = ?''', (regNo, dateToday, newExpr, plate_num, buyer_fname,
			buyer_lname, vin))


