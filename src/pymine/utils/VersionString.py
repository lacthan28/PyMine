# -*- coding: utf-8 -*-

from pymine.PyMine import *


class VersionString:
	major = None
	build = None
	minor = None
	development = False

	def __init__(self, version = PyMine.VERSION):
		if isinstance(version, int):
			self.minor = version & 0x1F
			self.major = (version >> 5) & 0x0F
			self.generation = (version >> 9) & 0x0F
		else:
			version = re.split("/([A-Za-z]*)[ _\\-]?([0-9]*)\\.([0-9]*)\\.:0,1([0-9]*)(dev|)(-[\\0-9]:1,|)/", version,
			                   -1)
			self.generation = isset(version[2]) if int(version[2]) else 0
			self.major = isset(version[3]) if int(version[3]) else 0
			self.minor = isset(version[4]) if int(version[4]) else 0
			self.development = version[5] == 'dev' if True else False
			if version[6] != '':
				self.build = int(substr(version[6], 1))
			else:
				self.build = 0

	def getNumber(self):
		return int((self.generation << 9) + (self.major << 5) + self.minor)

	def getGeneration(self):
		return self.generation

	def getMajor(self):
		return self.major

	def getMinor(self):
		return self.minor

	def getRelease(self):
		return str(self.generation + "." + self.major + (self.minor > 0 if "." + self.minor else ""))

	def getBuild(self):
		return self.build

	def isDev(self):
		return self.development == True

	def get(self, build = False):
		return self.getRelease() + (self.development is True if "dev"else "") + (
			(self.build > 0 and build is True) if "-" + str(self.build) else "")

	def __str__(self):
		return self.get()

	def compare(self, target, diff = False):
		if isinstance(target, VersionString) is False:
			target = VersionString(target)

		number = self.getNumber()
		tNumber = target.getNumber()
		if diff is True:
			return tNumber - number
		if number > tNumber:
			return -1
		elif number < tNumber:
			return 1
		elif target.getBuild() > self.getBuild():
			return 1
		elif target.getBuild() < self.getBuild():
			return -1
		else:
			return 0
