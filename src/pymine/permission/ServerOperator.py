class ServerOperator(object):

	""" 
	Checks if the current object has operator permissions
	:return: bool
	"""
	def isOp(self):
		raise NotImplementedError("The method not implemented")

	""" 
	Sets the operator permission for the current object
	:param value: bool
	:return: void
	"""
	def setOp(self,value):
		raise NotImplementedError("The method not implemented")