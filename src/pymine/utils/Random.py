# -*- coding: utf-8 -*-
from time import time


class Random:
	X = 123456789
	Y = 362436069
	Z = 521288629
	W = 88675123

	x = int
	y = int
	z = int
	w = int

	seed = None

	def __init__(self, seed = -1):
		if seed == -1:
			seed = time()

		self.setSeed(seed)

	def setSeed(self, seed):
		self.seed = seed
		self.x = Random.X ^ seed
		self.y = Random.Y ^ (seed << 17) | ((seed >> 15) & 0x7fffffff) & 0xffffffff
		self.z = Random.Z ^ (seed << 30) | ((seed >> 1) & 0x7fffffff) & 0xffffffff
		self.w = Random.W ^ (seed << 18) | ((seed >> 14) & 0x7fffffff) & 0xffffffff

	def getSeed(self):
		return self.seed

	def nextInt(self):
		return self.nextSignedInt() & 0x7fffffff

	def nextSignedInt(self):
		t = (self.x ^ (self.x << 11)) & 0xffffffff

		self.x = self.y
		self.y = self.z
		self.z = self.w
		self.w = (self.w ^ ((self.w >> 19) & 0x7fffffff) ^ (t ^ ((t >> 8) & 0x7fffffff))) & 0xffffffff

		return self.w

	def nextFloat(self):
		return self.nextInt() / 0x7fffffff

	def nextSignedFloat(self):
		return self.nextSignedInt() / 0x7fffffff

	def nextBoolean(self):
		return (self.nextSignedInt() & 0x01) == 0

	def nextRange(self, start = 0, end = 0x7fffffff):
		return start + (self.nextInt() % (end + 1 - start))

	def nextBoundedInt(self, bound):
		return self.nextInt() % bound
