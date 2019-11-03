from agent.methods.helpers import *
from dateutil.relativedelta import relativedelta

# Processes a bill of sale
# Inputs: cursor - an instance of the cursor object connected to the database
def processBOS(cursor):
    
    # Print info and check if agent has all the required information
    print("Processing a bill of sale...")
    print("You will need the vin, name of the current owner, " + 
        "name of the new owner, and a plate number for the new" +
        " registration")

    # Abort if agent doesn't have the required info
    if not promptMessage("- Do you have all this information?"):
        print("Returning to main menu")
        return

    # Get the vin of the car being sold
    vin = input("- What is the VIN of the vehicle\n> ")

    # Get the buyer a seller's name, abort if agent could not properly
    # fill out any of the names
    seller_fname = getName("- What is the seller's first name?\n")
    if not seller_fname:
        print("Returning to main menu")
        return

    seller_lname = getName("- What is the seller's last name?\n")
    if not seller_lname:
        print("Returning to main menu")
        return

    buyer_fname = getName("- What is the buyer's first name?\n")
    if not buyer_fname:
        print("Returning to main menu")
        return

    buyer_lname = getName("- What is the buyer's last name?\n")
    if not buyer_lname:
        print("Returning to main menu")
        return

    # Get the new plate number
    plate_num = input("- What is the new plate number?\n> ")

    # Get the first name and last name attached to the car
    statement = (
        "SELECT fname, lname "
        "FROM registrations "
        "WHERE vin = ? "
        "ORDER BY regdate DESC LIMIT 1"
    )
    cursor.execute(statement, (vin,))

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
    
    # Abort if there is incorrect information
    if not promptMessage("Is all this information correct?"):
        print("Returning to main menu")
        return

    # Get today's date as date time
    dateToday = datetime.date.today()
    
    # Add one year from today's date
    newExpr = dateToday + relativedelta(years=+1)
    
    # Generate a registration number
    regNo = genRegNo("registrations", cursor)
    
    # Update the current record with all the new info
    statement = (
        "INSERT INTO registrations "
        "VALUES(?,?,?,?,?,?,?)"
    )
    cursor.execute(statement, (regNo, dateToday, newExpr, plate_num, vin, buyer_fname,
            buyer_lname))

    # cursor.execute('''UPDATE registrations SET regno = ?, 
    #     regdate = ?, expiry = ?, plate = ?, fname = ?, lname = ? WHERE
    #     vin = ?''', (regNo, dateToday, newExpr, plate_num, buyer_fname,
    #         buyer_lname, vin))