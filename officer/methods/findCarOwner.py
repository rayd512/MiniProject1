from agent.methods.helpers import promptMessage, getName, getDate
from collections import OrderedDict

def findCarOwner(cursor):
    #Use an ordered dict to store the optional values
    values = OrderedDict()
    print("- Finding owner of car. Please provide information for one or more fields:")
    
    #Get the make
    print("Make:")
    make = input("> ")
    if make:
        values["make"] = make

    #Get the model
    print("Model:")
    model = input("> ")
    if model:
        values["model"] = model

    #Get the year of the car, check when an input was stored whether the input
    #is a valid year or not
    print("Year:")
    year = input("> ")
    if year.isdigit():
        values["year"] = year
    elif year:
        while True:
            if promptMessage("Year is not numeric, would you like to try again?"):
                print("Year:")
                year = input("> ")
                if year.isdigit():
                    values["year"] = year
                    break
            else:
                break

    #Get the color
    print("Color:")
    color = input("> ")
    if color:
        values["color"] = color

    #Get the plate number
    print("Plate:")
    plate = input("> ")
    if plate:
        values["plate"] = plate
    
    #If the user did not input any information, return to the main menu
    if not values:
        print("You must enter at least 1 piece of information about the car")
        print("Returning to the main menu")
        return

    #Create the SQL statement using safe string builder to prevent SQL injections
    if not plate:
        statement = "Select * from vehicles where "
    else:
        statement = (
            "SELECT vehicles.* "
            "FROM vehicles, registrations "
            "WHERE registrations.vin = vehicles.vin "
            "AND "
        )

    i = 0
    for value in values:
        if (i == len(values) - 1):
            statement += value + " LIKE ?"
        else:
            statement += value + " LIKE ? AND "
        i += 1

    #After building the statement, fetch all the results
    cursor.execute(statement, tuple(values.values()))
    results = cursor.fetchall()

    #Query for extra details depending on whether 4 or more matches were
    #found or not
    extraDetails = []
    if len(results) >= 4:
        statement = (
            "SELECT plate from registrations, vehicles "
            "WHERE vehicles.vin = ? "
            "AND registrations.vin = vehicles.vin "
            "ORDER BY registrations.regdate DESC LIMIT 1"
        )
        for i in range(len(results)):
            cursor.execute(statement, (results[i][0], ))
            extraDetails.append(cursor.fetchone())
    else:
        statement = (
            "SELECT plate, regdate, expiry, fname, lname from registrations, vehicles "
            "WHERE vehicles.vin = ? "
            "AND registrations.vin = vehicles.vin "
            "ORDER BY registrations.regdate DESC LIMIT 1"
        )
        for i in range(len(results)):
            cursor.execute(statement, (results[i][0], ))
            extraDetails.append(cursor.fetchone())

    #If there were 4 or more results, get the user to choose one of the cars
    #that were found. If the user chose a number, print more details about the chosen car
    carNum = 0
    if len(results) >= 4:
        print("Please select the number of one of the cars below to show further details.")
        print("Number|Make|Model|Year|Color|Plate")
        for i in range(len(results)):
            toPrint = (
                str(i+1) +
                "|" +
                '|'.join(str(v) for v in results[i][1:]) +
                "|" +
                (extraDetails[i][0] if extraDetails[i] else "Car has never been registered before")
            )
            print(toPrint)
        
        #Check if carNum is a valid digit
        carNum = input("> ")
        if not carNum.isdigit():
            while True:
                if promptMessage("Not a digit, would you like to retry to proceed?"):
                    carNum = input("> ")
                    if carNum.isdigit():
                        break
                else:
                    print("Returning to main menu")
                    return

        #Check if carNum is within the list bounds
        carNum = int(carNum) - 1      
        if carNum > len(results) - 1:
            print("Not a valid choice")
            print("Returning to main menu")
            return
        
        #Get the plate, registration and expiration date, and the full name of the owner
        #of the vehicle, and print them out to the user
        statement = (
        "SELECT plate, regdate, expiry, fname, lname from registrations, vehicles "
        "WHERE vehicles.vin = ? "
        "AND registrations.vin = vehicles.vin "
        "ORDER BY registrations.regdate DESC LIMIT 1"
        )
        cursor.execute(statement, (results[carNum][0], ))
        extraDetails = cursor.fetchone()
        print("Make|Model|Year|Color|Plate|Registration Date|Expiry Date|First Name|Last Name")
        toPrint = (
            '|'.join(str(v) for v in results[carNum][1:]) +
            "|" +
            ('|'.join(str(v) for v in extraDetails) if extraDetails else "Car has never been registered before")
        )
        print(toPrint)
    else:
        #Get the plate, registration and expiration date, and the full name of the owner
        #of the vehicle, and print them out to the user in case less than 4 matches were found
        print("Make|Model|Year|Color|Plate|Registration Date|Expiry Date|First Name|Last Name")
        for i in range(len(results)):
            toPrint = (
                '|'.join(str(v) for v in results[i][1:]) +
                "|" +
                ('|'.join(str(v) for v in extraDetails[i]) if extraDetails[i] else "Car has never been registered before")
            )
            print(toPrint)    