
class Officer:
	def __init__(self, uid, cursor):
		self.uid = uid
		self.loggedIn = True
		self.cursor = cursor
		print("Welcome Officer")
	
	def logout(self):
		self.loggedIn = False

	def processJobs(self):
		pass