from agent.methods.helpers import *
from dateutil.relativedelta import relativedelta
from datetime import datetime

# Renews a vehicle registration
# Inputs: cursor - an instance of the cursor object connected to the database
def renewVReg(cursor):

    print("Renewing a vehicle registration...")
    print("You will need the registration no.")

    # Abort if agent doesn't have the required info
    if not promptMessage("- Do you have this info?"):
        print("Returning to main menu")
        return

    # Get the registration number and check that it is only made up of numbers
    while True:
        regNo = input("- What is the vehicle registration number?\n")
        if not regNo.isdigit():
            resume = promptMessage("- Vehicle registration number can only" + 
                " digits. Would you like to try again?")
            if not resume:
                print("Returning to main menu")
                return
        else:
            break

    # Find the expiry date of the registration
    cursor.execute('''SELECT expiry FROM registrations WHERE regno = ?''', (regNo,))
    # Fetch the query result
    regExpr = cursor.fetchone()

    if regExpr is None:
        print("Could not find registration number")
        print("Returning to main menu")
        return
    # Convert expiry to a datetime object
    currentExpr = datetime.strptime(regExpr[0], '%Y-%m-%d')
    # Get today's date as date time
    dateToday = datetime.now()
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