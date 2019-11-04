from user import User
from officer.methods.issueTicket import issueTicket
from officer.methods.findCarOwner import findCarOwner

class Officer(User):
	def __init__(self, uid, cursor, connection):
		super().__init__(uid, cursor, connection)
		print("Welcome Officer " + super().getName())

	def dispOfficerActions(self):
		print("Type 'issueTicket' to register a birth")
		print("Type 'findCarOwner' to register a marriage")
		print("Type 'logout' to logout the program")
		print("Type 'exit' to exit the program")

	def processJobs(self):
		action = input("- What would you like to do. Type help to display options\n> ").lower()
		if action == 'help':
			self.dispOfficerActions()
		elif action == 'exit':
			super().exit()
		elif action == 'logout':
			super().logout()
		elif action == 'issueticket':
			issueTicket(self.cursor)
		elif action == 'findcarowner':
			findCarOwner(self.cursor)
		else:
			print("Unknown Command")	
		self.connection.commit()		