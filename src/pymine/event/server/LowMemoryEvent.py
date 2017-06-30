# -*- coding: utf-8 -*-
from pymine.utils.Utils import Utils


class LowMemoryEvent:
	handlerList = None

	__memory = None
	__memoryLimit = None
	__triggerCount = None
	__global = None

	def __init__(self, memory, memoryLimit, isGlobal=False, triggerCount = 0):
		self.__memory = memory
		self.__memoryLimit = memoryLimit
		self.__global = bool(isGlobal)
		self.__triggerCount = int(triggerCount)

	def getMemory(self)->int:
		return self.__memory

	def getMemoryLimit(self)->int:
		return self.__memoryLimit

	def getTriggerCount(self)->int:
		return self.__triggerCount

	def isGlobal(self)->bool:
		return self.__global

	def getMemoryFreed(self)->int:
		return self.getMemory() - (self.isGlobal() if Utils.getMemoryUsage(True)[1] else Utils.getMemoryUsage(True)[0])
