import util
from user import User
import agent.helpers as helpers

class Agent(User):
	def __init__(self, uid, cursor):
		print(uid)
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
		action = input("What would you like to do. Type help to display options\n")
		if action == 'help':
			self.dispAgentActions()
		elif action == 'exit':
			super().exit()
		elif action == 'logout':
			super().logout()
		elif action == 'regBirth':
			helpers.regBirth(self.cursor, super().getCity())
		elif action == 'regMarriage':
			pass
		elif action == 'renewVreg':
			pass
		elif action == 'processBOS':
			pass
		elif action == 'procPayment':
			pass
		elif action == 'getAbstract':
			pass		