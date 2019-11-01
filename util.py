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
		if(any(char.isdigit() for char in response) or
			response.isspace() or response == ""):
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

	bplace = input("Where was the baby born?\n")
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

# Registers a marriage into the database
# Inputs: cursor - an instance of the cursor object connected to the database
#		  city   - the city where the agent is in
def regMarriage(cursor, city):
	# Display info and confirm agent has all the required info for the
	# registration
	print("Registering a marriage...")
	print("You will need both partners full names.")
	resume = promptMessage("Do you have all this information ready?")

	# Get partner one's full name
	p1_fname, resume = getName("What is partner one's first name?\n")
	# Check if agent aborted
	if(resume == False):
		print("Returning to main menu")
		return

	# Check if agent aborted
	p1_lname, resume = getName("What is partner one's last name?\n")
	if(resume == False):
		print("Returning to main menu")
		return

	# Check if partner one is in the database, register them if not
	isRegistered = checkPerson(p1_fname, p1_lname, cursor)
	if isRegistered == False:
		handleNotReg(p1_fname, p1_lname, cursor)

	# Get partner two's full name
	p2_fname, resume = getName("What is partner two's first name?\n")

	# Check if agent aborted
	if(resume == False):
		print("Returning to main menu")
		return

	p2_lname, resume = getName("What is partner two's last name?\n")

	# Check if agent aborted
	if(resume == False):
		print("Returning to main menu")
		return

	# Check if partner one is in the database, register them if not
	isRegistered = checkPerson(p2_fname, p2_lname, cursor)
	if isRegistered == False:
		handleNotReg(p2_fname, p2_lname, cursor)

	# Confirm the information
	print("Please confirm the following information")
	print("Partner 1 Full name: " + p1_fname + " " + p1_lname)
	print("Partner 2 Full name: " + p2_fname + " " + p2_lname)
	resume = promptMessage("Is all this information correct?")
	# Abort process if information is not correct
	if resume == False:
		print("Returning to main menu")
		return

	# Generate a unique registration number
	regNo = genRegNo("marriages", cursor)

	# Get today's date
	regdate = datetime.datetime.date(datetime.datetime.now())

	cursor.execute('''INSERT INTO marriages VALUES (?,?,?,?,?,?,?)''',
		(regNo, regdate, city, p1_fname, p1_lname, p2_fname, p2_lname))

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
	seller_fname, resume = getName("What is the seller's first name?\n")
	if(resume == False):
		print("Returning to main menu")
		return

	seller_lname, resume = getName("What is the seller's last name?\n")
	if(resume == False):
		print("Returning to main menu")
		return

	buyer_fname, resume = getName("What is the buyer's first name?\n")
	if(resume == False):
		print("Returning to main menu")
		return

	buyer_lname, resume = getName("What is the buyer's last name?\n")
	if(resume == False):
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


