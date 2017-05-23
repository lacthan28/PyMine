import thread, collections

class Collectable(object):
	
	def __init__(self):
		self.isGarb = False

	def isGarbage(self):
		return self.isGarb

	def setGarbage(self):
		self.isGarb = True