# coding=utf-8
import hashlib

from pymine.Server import Server
from pymine.entity.Living import Living


class TimingsHandler:
	"""
	:param dict HANDLERS: TimingsHandler[]
	:param TimingsHandler parent:
	"""
	HANDLERS = dict()

	name = None

	parent = None

	count = 0
	curCount = 0
	start = 0
	timingDepth = 0
	totalTime = 0
	curTickTotal = 0
	violations = 0

	def __init__(self, name, parent = None):
		"""

		:param str name:
		:param TimingsHandler parent:
		"""
		self.name = name
		if parent is not None:
			self.parent = parent

		TimingsHandler.HANDLERS[hash(self)] = self

	@staticmethod
	def printTimings(fp):
		file = open(fp)
		file.write("Minecraft\n")

		for timings in TimingsHandler.HANDLERS:
			time = timings.totalTime
			count = timings.count
			if count == 0:
				continue
			avg = time / count

			file.write(
					"    " + timings.name + " Time: " + str(
							round(time * 1000000000)) + " Count: " + count + " Avg: " + str(
							round(avg * 1000000000)) + " Violations: " + timings.violations + "\n")
		file.write("# Version " + Server.getInstance().getVersion() + "\n")
		file.write("# " + Server.getInstance().getName() + " " + Server.getInstance().getPocketMineVersion() + "\n")

		entities = 0
		livingEntities = 0
		for level in Server.getInstance().getLevels():
			entities += len(level.getEntities())
			for e in level.getEntities():
				if isinstance(e, Living):
					livingEntities += 1
