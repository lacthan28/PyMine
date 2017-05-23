from permission import ServerOperator
class IPlayer(ServerOperator):
	
	# :return: bool
	def isOnline():
		raise NotImplementedError("The method not implemented")

	# :return: String
	def getName():
		raise NotImplementedError("The method not implemented")

	# :return: bool
	def isBanned():
		raise NotImplementedError("The method not implemented")

	# :param banned: bool
	def setBanned(banned):
		raise NotImplementedError("The method not implemented")

	# :return: bool
	def isWhitelisted():
		raise NotImplementedError("The method not implemented")

	# :param value: bool
	def setWhitelisted(value):
		raise NotImplementedError("The method not implemented")

	# :return: Player|null
	def getPlayer():
		raise NotImplementedError("The method not implemented")

	# :return: int|double
	def getFirstPlayed():
		raise NotImplementedError("The method not implemented")

	# :return: int|double
	def getLastPlayed():
		raise NotImplementedError("The method not implemented")

	# :return: mixed
	def hasPlayedBefore():
		raise NotImplementedError("The method not implemented")