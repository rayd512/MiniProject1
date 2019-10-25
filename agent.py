import util
def agentActions(uid, cursor):
	# Find the agents name
	cursor.execute('''SELECT fname, city FROM users where uid =?''', (uid,))
	agentInfo = cursor.fetchone()
	# Personally welcome the agent
	print("Welcome Agent " + agentInfo[0])
	# Prompt the agaent what he'd like to do today
	action = input("What would you like to do today? Type help for options\n").lower()
	# Boolean that holds if more actions are to be made
	newAction = False
	# Match the input to the appropriate action
	while True:
		if action == "regbirth":
			# Call function from util.py here
			util.regBirth(cursor, agentInfo[1])
		elif action == "regmarriage":
			util.regMarriage(cursor, agentInfo[1])
		elif action == "renewvreg":
			util.renewVReg(cursor)
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
		action = input("Next action? \n").lower()
	print("Goodbye Agent " + agentInfo[0])