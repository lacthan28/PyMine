# -*- coding: utf-8 -*-

class Range:
	minValue = None
	maxValue = None

	def __init__(self, minValue: int, maxValue: int):
		self.minValue = minValue
		self.maxValue = maxValue

	def isInRange(self, v: int) -> bool:
		return self.minValue <= v <= self.maxValue
