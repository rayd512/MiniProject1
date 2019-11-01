from agent.methods.helpers import *
import datetime

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
	fname = getName("What is the baby's first name?\n")
	if not fname:
		print("Returning to main menu")
		return

	# Get the last name of the baby
	lname = getName("What is the baby's last name?\n")
	if not lname:
		print("Returning to main menu")
		return

	# Get the gender of the baby, will check if something other than
	# 'm' or 'f' is entered and will ask the user if it wants to try again
	while True:
		gender = input("> What is the baby's gender? (m/f)\n").lower()
		if (gender == "m" or gender == "f"):
			break
		else:
			if not promptMessage("Unknown gender, try again?"):
				print("Returning to main menu")
				return

	# Get a valid birthday
	bday = getDate()
	if not bday:
		print("Returning to main menu")
		return

	bplace = input("> Where was the baby born?\n")

	# Get the mother's first name
	m_fname = getName("What is the mother's first name? \n")	
	if not m_fname:
		print("Returning to main menu")
		return
	
	# Get the mother's last name
	m_lname = getName("What is the mother's last name? \n")
	if not m_lname:
		print("Returning to main menu")
		return
	
	#Check if mother exists in the DB
	if not checkPerson(m_fname, m_lname, cursor):
		isRegMother = False
		handleNotReg(m_fname, m_lname, cursor)

	# Get the father's first name
	f_fname = getName("What is the father's first name? \n")
	if not f_fname:
		print("Returning to main menu")
		return

	# Get the father's last name
	f_lname = getName("What is the father's last name? \n")
	if not f_lname:
		print("Returning to main menu")
		return

	# Check for registration of the father in the database, add him
	# if he is not in the database
	if not checkPerson(f_fname, f_lname, cursor):
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
	if (not resume):
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