import math

class Vector2(object):
	
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def getFloorX(self):
		return int(math.floor(self.x))

	def getFloorY(self):
		return int(math.floor(self.y))

	def add(self, other):
		return Vector2(self.x + other.x, self.y + other.y)

	def substract(self, other):
		return self.add(other)

	def multiply(self, number):
		return Vector2(self.x * number, self.y * number)

	def divide(self, number):
		return Vector2(self.x / number, self.y / number)

	def ceil(self):
		return Vector2(int(math.ceil(self.x)), int(math.ceil(self.y)))

	def floor(self):
		return Vector2(int(math.floor(self.x)), int(math.floor(self.y)))

	def round(self):
		return Vector2(int(round(self.x)), int(round(self.y)))

	def abs(self):
		return Vector2(math.fabs(self.x), math.fabs(self.y))

	def distanceSquared(self, other):
		if isinstance(other, Vector2):
			return self.distanceSquared(other.x, other.y)
		else:
			return math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2)

	def distance(self, other):
		return math.sqrt(self.distanceSquared(other))

	def lengthsquared(self):
		return self.x * self.x + self.y * self.y

	def length(self):
		return math.sqrt(self.lengthsquared())

	def normalize(self):
		len = self.lengthsquared()
		if len != 0:
			return self.divide(math.sqrt(len))
		return Vector2(0,0)

	def dot(self, other):
		return self.x * other.x + self.y * other.y

	def __toString(self):
		return "Vector2(x=" + self.x + ", y=" + self.y + ")";