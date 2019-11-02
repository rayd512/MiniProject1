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
    tno = input("What is the ticket number? \n")

    # Search for the tno
    cursor.execute('''SELECT tno FROM tickets WHERE tno = ?''', (tno,))
    tno = cursor.fetchone()

    # Check if tno exists
    if not tno:
        print("Could not find ticket number")
        return

    # Get the payment amount
    amount = getPaymentAmount()

    # If the amount was invalid
    if not amount:
        print("Returning to main menu")
        return

    # Get the fine amount
    cursor.execute('''SELECT fine from tickets where tno = ?''', (tno,))
    fineAmount = cursor.fetchone()

    # Check if the payment amount does not exceed the fine amount left to pay
    if amount > fineAmount[0]:
        print("Could not process payment, amount is greater than the fine")
        return

    # Get today's date
    pdate = datetime.date.today()
    # Add the payment to the tables
    cursor.execute('''INSERT INTO payments VALUES (?,?,?)''', (tno, pdate, amount))

    # Get the remaining balance left
    remBal = fineAmount[0] - amount
    # Update the fine amount left
    cursor.execute('''UPDATE tickets SET fine = ? WHERE tno = ?''', (remBal, tno))
