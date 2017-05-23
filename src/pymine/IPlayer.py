from permission import ServerOperator
class IPlayer(ServerOperator):
	
	# :return: bool
	def isOnline(self):
		raise NotImplementedError("The method not implemented")

	# :return: String
	def getName(self):
		raise NotImplementedError("The method not implemented")

	# :return: bool
	def isBanned(self):
		raise NotImplementedError("The method not implemented")

	# :param banned: bool
	def setBanned(self, banned):
		raise NotImplementedError("The method not implemented")

	# :return: bool
	def isWhitelisted(self):
		raise NotImplementedError("The method not implemented")

	# :param value: bool
	def setWhitelisted(self, value):
		raise NotImplementedError("The method not implemented")

	# :return: Player|null
	def getPlayer(self):
		raise NotImplementedError("The method not implemented")

	# :return: int|double
	def getFirstPlayed(self):
		raise NotImplementedError("The method not implemented")

	# :return: int|double
	def getLastPlayed(self):
		raise NotImplementedError("The method not implemented")

	# :return: mixed
	def hasPlayedBefore(self):
		raise NotImplementedError("The method not implemented")