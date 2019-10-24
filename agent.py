import util
def agentActions(uid, cursor):
	cursor.execute('''SELECT fname FROM users where uid =?''', (uid,))
	agentName = cursor.fetchone()
	print("Welcome Agent " + agentName[0])
	action = input("What would you like to do today? Type help for options\n").lower()
	newAction = False
	while True:
		if action == "regbirth":
			# Call function from util.py here
			pass
		elif action == "regmarriage":
			pass
		elif action == "renewvreg":
			pass
		elif action == "processbos":
			pass
		elif action == "procpayment":
			pass
		elif action == "getAbstract":
			pass
		elif action == "help":
			util.dispAgentActions()
			# break # Temporary
		elif action == "exit":
			break
		elif action == "logout":
			pass
		else:
			print("Unknown Command: Please try again")

		# newAction = util.promptMessage()
		# if newAction == True:
		# 	action = input("Next Action?\n")
		# else:
		# 	break
		action = input("Next action? \n")