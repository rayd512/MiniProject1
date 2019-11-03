from agent.methods.helpers import promptMessage, getName, getDate
from datetime import datetime

def issueTicket(cursor):
    print("Issuing a ticket...")
    print("You will need a registration number to register the ticket to")

    if not promptMessage("- Do you have this information?"):
        print("Returning to main menu")
        return
    
    regNo = input("- What is the registration number?\n> ")

    if (not regNo) or not (regNo.isdigit()):
        if not promptMessage("Invalid registration number. Would you like to try again?"):
            print("Returning to main menu")
            return

    statement = (
        "SELECT registrations.fname, registrations.lname, vehicles.make, vehicles.model, " 
        "vehicles.year, vehicles.color " 
        "FROM registrations, vehicles " 
        "WHERE registrations.regno = ? AND registrations.vin = vehicles.vin"
    )

    cursor.execute(statement, (regNo, ))
    result = cursor.fetchone()

    if not result:
        print("Registration not found")
        print("Returning to main menu")
        return
    
    print("Name: " + result[0] + " " + result[1])
    print("Car Make: " + result[2] + ", Model: " + result[3] + ", Year: " + 
            str(result[4]) + ", Color: " + result[5])
    
    if not promptMessage("- Is this the right information?"):
        print("Returning to main menu")
        return
    
    while True:
        print("- What is the violation date?")
        print("To use today's date, press enter.")
        print("Otherwise, enter the date in the format 'year-month-day', i.e., 1999-05-12")
        violDate = input("> ")
        if not violDate:
            violDate = datetime.date(datetime.now())
            break
        else:
            try:
                datetime.strptime(violDate, '%Y-%m-%d')
                break
            except ValueError:
                if not promptMessage("Incorrect date format, try again?"):
                    return
    

    violDescr = input("- Enter a description for the ticket\n> ")

    fine = input("- Enter fine amount\n> ") 
    while (not fine) or not(fine.isdigit()):
        if not promptMessage("Invalid fine amount. Would you like to try again?"):
            print("Returning to main menu")
            return
        fine = input("- Enter fine amount") 
    
    cursor.execute("SELECT count(*) FROM tickets")
    tno = cursor.fetchone()[0]

    statement = "INSERT INTO tickets(tno, regno, fine, violation, vdate) VALUES(?, ?, ?, ?, ?)"
    args = (tno, regNo, fine, violDescr, violDate)    
    cursor.execute(statement, args)
        
        

        





