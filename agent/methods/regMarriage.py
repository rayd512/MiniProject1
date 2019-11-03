from agent.methods.helpers import *
from datetime import datetime

# Registers a marriage into the database
# Inputs: cursor - an instance of the cursor object connected to the database
#		  city   - the city where the agent is in
def regMarriage(cursor, city):
    # Display info and confirm agent has all the required info for the
    # registration
    print("Registering a marriage...")
    print("You will need both partners full names.")

    if not promptMessage("- Do you have all this information ready?"):
        print("Returning to main menu")
        return

    # Get partner one's full name
    p1_fname = getName("- What is partner one's first name?\n")
    # Check if agent aborted
    if not p1_fname:
        print("Returning to main menu")
        return

    # Check if agent aborted
    p1_lname = getName("- What is partner one's last name?\n")
    if not p1_lname:
        print("Returning to main menu")
        return

    # Check if partner one is in the database, register them if not
    if not checkPerson(p1_fname, p1_lname, cursor):
        handleNotReg(p1_fname, p1_lname, cursor)

    # Get partner two's full name
    p2_fname = getName("- What is partner two's first name?\n")

    # Check if agent aborted
    if not p2_fname:
        print("Returning to main menu")
        return

    p2_lname = getName("- What is partner two's last name?\n")

    # Check if agent aborted
    if not p2_lname:
        print("Returning to main menu")
        return

    # Check if partner one is in the database, register them if not
    if not checkPerson(p2_fname, p2_lname, cursor):
        handleNotReg(p2_fname, p2_lname, cursor)

    # Confirm the information
    print("Please confirm the following information")
    print("Partner 1 Full name: " + p1_fname + " " + p1_lname)
    print("Partner 2 Full name: " + p2_fname + " " + p2_lname)

    # Abort process if information is not correct
    if not promptMessage("- Is all this information correct?"):
        print("Returning to main menu")
        return

    # Generate a unique registration number
    regNo = genRegNo("marriages", cursor)

    # Get today's date
    regdate = datetime.date(datetime.now())

    cursor.execute('''INSERT INTO marriages VALUES (?,?,?,?,?,?,?)''',
        (regNo, regdate, city, p1_fname, p1_lname, p2_fname, p2_lname))