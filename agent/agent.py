import util
import sys
from user import User
from agent.methods.regBirth import regBirth

class Agent(User):
	def __init__(self, uid, cursor):
		super().__init__(uid, cursor)
		print("Welcome Agent")
	
	def dispAgentActions(self):
		print("Type 'regBirth' to register a birth")
		print("Type 'regMarriage' to register a marriage")
		print("Type 'renewVreg' to renew a vehicle registration")
		print("Type 'processBOS' to process a bill of sale")
		print("Type 'procPayment' to process a payment")
		print("Type 'getAbstract' to get a driver abstract")
		print("Type 'logout' to logout the program")
		print("Type 'exit' to exit the program")

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
			pass
		elif action == 'renewvreg':
			pass
		elif action == 'processbos':
			pass
		elif action == 'procpayment':
			pass
		elif action == 'getabstract':
			pass		