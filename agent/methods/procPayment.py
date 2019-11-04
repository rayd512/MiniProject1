from agent.methods.helpers import *

def procPayment(cursor):
    # Display info
    print("Processing a payment...")
    print("You will need the ticket number and the payment amount")

    # Check if agent has all this information
    if not promptMessage("Do you have all this information ready?"):
        print("Returning to main menu")
        return

    # Get the ticket number from the agent
    tno = input("What is the ticket number? \n> ")

    # Check if tno is a digit, return to main if not
    if not tno.isdigit():
        print("Invalid ticket number")
        print("Returning to main menu")
        return

    # Search for the tno
    cursor.execute('''SELECT tno, fine FROM tickets WHERE tno = ?''', (tno,))
    ticketInfo = cursor.fetchone()

    # Get today's date
    pdate = datetime.date.today()

    # Check the payments table from previous ticket payments
    cursor.execute('''SELECT pdate
                    FROM payments
                    WHERE tno = ?''',
                    (tno,))

    paymentInfo = cursor.fetchone()

    # Check if a payment has already been processed today
    if paymentInfo is not None:
        paymentDate = datetime.datetime.strptime(paymentInfo[0], '%Y-%m-%d').date()
        if paymentDate == pdate:
            print("A transaction has already been processed today, try again tomorrow")
            print("Returning to main menu")
            return

    # Check if tno exists
    if not ticketInfo:
        print("Could not find ticket number")
        return

    # Get the payment amount
    amount = getPaymentAmount()

    # If the amount was invalid
    if not amount:
        print("Returning to main menu")
        return

    # Check if the payment amount does not exceed the fine amount left to pay
    if  int(amount) > ticketInfo[1]:
        print("Could not process payment, amount is greater than the fine")
        return


    # Add the payment to the tables
    cursor.execute('''INSERT INTO payments VALUES (?,?,?)''', (tno, pdate, amount))

    # Get the remaining balance left
    remBal = ticketInfo[1] - int(amount)
    # Update the fine amount left
    cursor.execute('''UPDATE tickets SET fine = ? WHERE tno = ?''', (remBal, tno))

    print("Transaction succesfully processed")