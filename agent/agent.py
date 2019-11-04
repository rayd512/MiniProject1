from user import User
from agent.methods.regBirth import regBirth
from agent.methods.regMarriage import regMarriage
from agent.methods.renewVreg import renewVReg
from agent.methods.processBOS import processBOS
from agent.methods.procPayment import procPayment
from agent.methods.getAbstract import getAbstract

class Agent(User):
	# Constructor
	def __init__(self, uid, cursor):
		super().__init__(uid, cursor)
		print("Welcome Agent " + self.getName())
	
	# Display the actions available to the agent
	def dispAgentActions(self):
		print("Type 'regBirth' to register a birth")
		print("Type 'regMarriage' to register a marriage")
		print("Type 'renewVreg' to renew a vehicle registration")
		print("Type 'processBOS' to process a bill of sale")
		print("Type 'procPayment' to process a payment")
		print("Type 'getAbstract' to get a driver abstract")
		print("Type 'logout' to logout the program")
		print("Type 'exit' to exit the program")

	# Process what the user wants to do and the call the appropriate function
	def processJobs(self):
		action = input("What would you like to do. Type help to display options\n> ").lower()
		if action == 'help':
			self.dispAgentActions()
		elif action == 'exit':
			super().exit()
		elif action == 'logout':
			super().logout()
		elif action == 'regbirth':
			regBirth(self.cursor, super().getCity())
		elif action == 'regmarriage':
			regMarriage(self.cursor, super().getCity())
		elif action == 'renewvreg':
			renewVReg(self.cursor)
		elif action == 'processbos':
			processBOS(self.cursor)
		elif action == 'procpayment':
			procpayment(self.cursor)
		elif action == 'getabstract':
			getAbstract(self.cursor)
		else:
			print("Unknown Command")