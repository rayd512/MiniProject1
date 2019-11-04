from agent.methods.helpers import promptMessage, getName, getDate
from collections import OrderedDict

def findCarOwner(cursor):
    values = OrderedDict()
    print("- Finding owner of car. Please provide information for one or more fields:")
    
    print("Make:")
    make = input("> ")
    if make:
        values["make"] = make

    print("Model:")
    model = input("> ")
    if model:
        values["model"] = model

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
            else:
                break

    print("Color:")
    color = input("> ")
    if color:
        values["color"] = color

    print("Plate:")
    plate = input("> ")
    if plate:
        values["plate"] = plate
    
    if not plate:
        statement = "Select * from vehicles where "
    else:
        statement = (
            "SELECT vehicles.*, registrations.plate "
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

    cursor.execute(statement, tuple(values.values()))
    results = cursor.fetchall()
    
    extraDetails = []
    if len(results) > 4:
        statement = (
            "SELECT plate from registrations, vehicles"
            "WHERE vehicles.vin = ?"
            "AND registrations.vin = vehicles.vin"
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

    carNum = 0
    if len(results) >= 2:
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

        carNum = int(carNum) - 1        
        statement = (
        "SELECT plate, regdate, expiry, fname, lname from registrations, vehicles "
        "WHERE vehicles.vin = ? "
        "AND registrations.vin = vehicles.vin "
        "ORDER BY registrations.regdate DESC LIMIT 1"
        )
        cursor.execute(statement, (results[carNum][0], ))
        extraDetails = cursor.fetchone()
        toPrint = (
            '|'.join(str(v) for v in results[carNum][1:]) +
            "|" +
            ('|'.join(str(v) for v in extraDetails) if extraDetails else "Car has never been registered before")
        )
        print(toPrint)
    else:
        print("Make|Model|Year|Color|Plate|Registration Date|Expiry Date|First Name|Last Name")
        for i in range(len(results)):
            toPrint = (
                '|'.join(str(v) for v in results[i][1:]) +
                "|" +
                ('|'.join(str(v) for v in extraDetails[i]) if extraDetails[i] else "Car has never been registered before")
            )
            print(toPrint)    
    
                    
    # for car in results:
    #     statement = "SELECT "
    # print(results)
