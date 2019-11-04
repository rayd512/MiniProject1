from agent.methods.helpers import *
from datetime import datetime

def issueTicket(cursor):
    print("Issuing a ticket...")
    print("You will need a registration number to register the ticket to")

    if not promptMessage("- Do you have this information?"):
        print("Returning to main menu")
        return

    # Get registration number
    while True:    
        regNo = input("- What is the registration number?\n> ")

        if (not regNo) or not (regNo.isdigit()):
            if not promptMessage("Invalid registration number. Would you like to try again?"):
                print("Returning to main menu")
                return
        else:
            break

    #Get the full name and vehicle's information from the DB
    statement = (
        "SELECT registrations.fname, registrations.lname, vehicles.make, vehicles.model, " 
        "vehicles.year, vehicles.color " 
        "FROM registrations, vehicles " 
        "WHERE registrations.regno = ? AND registrations.vin = vehicles.vin"
    )
    cursor.execute(statement, (regNo, ))
    result = cursor.fetchone()

    #If result is empty (i.e. registration not found), print error message and return to main menu
    if not result:
        print("Registration not found")
        print("Returning to main menu")
        return
    
    #Print the information that was received about the car
    print("Name: " + result[0] + " " + result[1])
    print("Car Make: " + result[2] + ", Model: " + result[3] + ", Year: " + 
            str(result[4]) + ", Color: " + result[5])
    
    #Check with the user that this is the right vehicle to ticket
    if not promptMessage("- Is this the right information?"):
        print("Returning to main menu")
        return
    
    #Get the violation date. If the user did not enter anything, then
    #use today's date. Otherwise, check if the date entered is in the future
    #and save the date / Exit
    while True:
        print("- What is the violation date?")
        print("To use today's date, press enter.")
        print("Otherwise, enter the date in the format 'year-month-day', i.e., 1999-05-12")
        today = datetime.date(datetime.now())
        violDate = input("> ")
        if not violDate:
            violDate = today
            break
        else:
            try:
                #Convert datetime to date from the input string
                violDate = datetime.strptime(violDate, '%Y-%m-%d').date()
                if violDate > today:
                    if not promptMessage("The date cannot be in the future, try again?"):
                        return
                    continue
                else:
                    break
            except ValueError:
                if not promptMessage("Incorrect date format, try again?"):
                    return
    
    #Get a description of the ticket
    violDescr = input("- Enter a description for the ticket\n> ")

    #Get the find amont of the ticket
    fine = input("- Enter fine amount\n> ") 
    while (not fine) or not(fine.isdigit()):
        if not promptMessage("Invalid fine amount. Would you like to try again?"):
            print("Returning to main menu")
            return
        fine = input("- Enter fine amount") 
    
    #Create a unique key for the table, by calling the helper method
    tno = genRegNo("tickets", cursor)

    #Finally, insert the new ticket into the DB
    statement = "INSERT INTO tickets(tno, regno, fine, violation, vdate) VALUES(?, ?, ?, ?, ?)"
    args = (tno, regNo, fine, violDescr, violDate)    
    cursor.execute(statement, args)
        
        

        





