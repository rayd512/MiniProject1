import util
def agentActions():
	print("Welcome Agent")
	action = input("What would you like to do today? Type help for options").lower()
	while True:
		if action == "register a birth":
			# Call function from util.py here
			pass
		elif action == "register a marriage":
			pass
		elif action == "renew a vehicle registration":
			pass
		elif action == "process a bill of sale":
			pass
		elif action == "process a payment":
			pass
		elif action == "get a driver abstract":
			pass
		elif action == "help":
			pass
		elif action == "exit":
			break
		else:
			print("Unknown Command: Please try again")