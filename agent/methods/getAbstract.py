from agent.methods.helpers import *

# Obtains a driver's abstract
def getAbstract(cursor):
	# Prompt information on to the screen
	print("Obtaining driver's abstract...")
	print("Please ensure you have the person's first name and last name")

	if not promptMessage("Do you have all this information ready?"):
		print("Returning to main menu")
		return

	# Get the person's name
	fName = getName("What is the first name?\n").lower().capitalize()
	lName = getName("What is the last name?\n").lower().capitalize()

	# Check if person exists in database
	if not checkPerson(fName, lName, cursor):
		print(fName + " " + lName + " is not in the records. Returning to main menu.")
		return

	cursor.execute('''
		SELECT rt.fname, rt.lname, tcount, dcount, sum(d1.points) 
		from(select r.fname, r.lname, COUNT(distinct tno) as tcount, COUNT(distinct ddate) as dcount
				from ( 
					(registrations r left join tickets t  on (r.regno = t.regno and vdate >= date('now', '-2 years'))) 
					left join demeritNotices d on (r.fname = ? and r.lname = ? and r.fname = d.fname and r.lname = d.lname and ddate >= date('now', '-2 years')) 
					)
				group by r.fname, r.lname) rt 
				left join demeritNotices d1 on (rt.fname = d1.fname and rt.lname = d1.lname and ddate >= date('now', '-2 years'))
		where rt.fname = ? and rt.lname = ?
		group by rt.fname, rt.lname
		''', (fName, lName, fName, lName))

	# records within past 2 years
	recent = cursor.fetchone()

	cursor.execute('''
		SELECT rt.fname, rt.lname, tcount, dcount, sum(d1.points) 
		from(select r.fname, r.lname, COUNT(distinct tno) as tcount, COUNT(distinct ddate) as dcount
				from ( 
					(registrations r left join tickets t  on (r.regno = t.regno)) 
					left join demeritNotices d on (r.fname = ? and r.lname = ? and r.fname = d.fname and r.lname = d.lname) 
					)
				group by r.fname, r.lname) rt 
				left join demeritNotices d1 on (rt.fname = d1.fname and rt.lname = d1.lname)
		where rt.fname = ? and rt.lname = ?
		group by rt.fname, rt.lname
		''', (fName, lName, fName, lName))

	# lifetime record
	lifetime = cursor.fetchone()

	if (lifetime == None):
		print(fName + " " + lName + " has no registration records. Returning to main menu.")
		print()
		return
		
	print()
	print("Viewing " + fName + " " + lName + "'s abstract summary (last 2 years/ lifetime): ")
	print("Name: " + str(recent[0]) + " " + str(recent[1]))
	print("Tickets: " + str(recent[2]) + "/" + str(lifetime[2]))
	print("Demerit Notices: " + str(recent[3]) + "/" + str(lifetime[3]))
	print("Demerit Points: " + str(recent[4]) + "/" + str(lifetime[4]))
	print()

	if not promptMessage("View " + fName + " " + lName + "'s ticket(s)?"):
		print("Returning to main menu")
		return 

	cursor.execute('''SELECT tno, vdate, violation, fine, r.regno, make, model
	FROM tickets t, registrations r, vehicles v
	WHERE t.regno = r.regno
	AND r.fname LIKE ? AND r.lname LIKE ?
	AND r.vin = v.vin
	ORDER BY vdate DESC
	''', (fName, lName))

	tickRecord = cursor.fetchall()

	recordLength = len(tickRecord)

	if recordLength == 0:
		print("No tickets to show")
		return

	if recordLength <= 5:
		print("Showing " + str(recordLength) + " of " + str(recordLength) + " tickets: ")
		for row in tickRecord:
			print(row)
		return

	start = 0
	end = 4
	remaining = recordLength
	while (remaining > 0):
		print("Showing " + str(end+1) + " of " + str(recordLength) + " tickets: ")
		for y in range(start, end+1):
			print()
			print("Ticket #: " + str(tickRecord[y][0]))
			print("Violation Date: " + str(tickRecord[y][1]))
			print("Violation: " + str(tickRecord[y][2]))
			print("$ Amount: " + str(tickRecord[y][3]))
			print("Registration #: " + str(tickRecord[y][4]))
			print("Make: " + str(tickRecord[y][5]))
			print("Model: " + str(tickRecord[y][6]))
			print()

		remaining = remaining - (end-start) - 1
		start += 5

		end = (end+5) if (remaining > 5) else (end+remaining)

		if (remaining > 0):
			if not promptMessage("View more tickets?"):
				print("Returning to main menu")
				return 