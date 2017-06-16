# -*- coding: utf-8 -*-
class AxisAlignedBB(object):
	minX = None
	minY = None
	minZ = None
	maxX = None
	maxY = None
	maxZ = None

	def __init__(self, minX, minY, minZ, maxX, maxY, maxZ):
		self.minX = minX
		self.minY = minY
		self.minZ = minZ
		self.maxX = maxX
		self.maxY = maxY
		self.maxZ = maxZ

	def setBounds(self, minX, minY, minZ, maxX, maxY, maxZ):
		self.minX = minX
		self.minY = minY
		self.minZ = minZ
		self.maxX = maxX
		self.maxY = maxY
		self.maxZ = maxZ

		return self
