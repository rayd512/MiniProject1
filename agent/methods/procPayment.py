from agent.methods.helpers import *

def procPayment(cursor):
    # Display info
    print("Processing a payment...")
    print("You will need the ticket number and the payment amount")

    # Check if agent has all this information
    if not promptMessage("Do you have all this information ready?"):
        print("Returning to main menu")
        return

    tno = input("What is the ticket number? \n")

    cursor.execute('''SELECT tno FROM tickets WHERE tno = ?''', (tno,))
    tno = cursor.fetchone()

    if not tno:
        print("Could not find ticket number")
        return

    amount = getPaymentAmount()

    if not amount:
        print("Returning to main menu")
        return

    cursor.execute('''SELECT fine from tickets where tno = ?''', (tno,))
    fineAmount = cursor.fetchone()

    if amount > fineAmount[0]:
        print("Could not process payment, amount is greater than the fine")
        return

    pdate = datetime.date.today()
    cursor.execute('''INSERT INTO payments VALUES (?,?,?)''', (tno, pdate, amount))

    remBal = fineAmount[0] - amount
    cursor.execute('''UPDATE tickets SET fine = ? WHERE tno = ?''', (remBal, tno))
