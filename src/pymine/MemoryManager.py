# -*- coding: utf-8 -*-
import configparser
import re

import gc

from pymine.Server import Server
from pymine.event.server.LowMemoryEvent import LowMemoryEvent
from pymine.level.Level import Level


class MemoryManager:
	__server = None

	__memoryLimit = None
	__globalMemoryLimit = None
	__checkRate = None
	__checkTicker = 0
	__lowMemory = False

	__continuousTrigger = True
	__continuousTriggerRate = None
	__continuousTriggerCount = 0
	__continuousTriggerTicker = 0

	__garbageCollectionPeriod = None
	__garbageCollectionTicker = 0
	__garbageCollectionTrigger = None
	__garbageCollectionAsync = None

	__chunkRadiusOverride = None
	__chunkCollect = None
	__chunkTrigger = None

	__chunkCache = None
	__cacheTrigger = None

	def __init__(self, server: Server):
		self.__server = server
		self.init()

	def init(self):
		self.__memoryLimit = (int(self.__server.getProperty("memory.main-limit", 0))) * 1024 * 1024

		defaultMemory = 1024

		matches = re.search("/([0-9]+)([KMGkmg])/", self.__server.getConfigString("memory-limit", ""))
		if matches is not None:
			m = int(matches.group(1))
			if m <= 0:
				defaultMemory = 0
			else:
				ma = matches.group(2)
				if ma == 'K':
					defaultMemory = m / 1024
				elif ma == 'M':
					defaultMemory = m
				elif ma == 'G':
					defaultMemory = m * 1024
				else:
					defaultMemory = m
		hardLimit = (int(self.__server.getProperty("memory.main-hard-limit", defaultMemory)))

		parser = configparser.ConfigParser()
		if hardLimit <= 0:
			parser.set('MEMORY', 'memory_limit', -1)
		else:
			parser.set('MEMORY', 'memory_limit', str(hardLimit) + 'M')

		self.__globalMemoryLimit = (int(self.__server.getProperty("memory.global-limit", 0))) * 1024 * 1024
		self.__checkRate = int(self.__server.getProperty("memory.check-rate", 20))
		self.__continuousTrigger = bool(self.__server.getProperty("memory.continuous-trigger", True))
		self.__continuousTriggerRate = int(self.__server.getProperty("memory.continuous-trigger-rate", 30))

		self.__garbageCollectionPeriod = int(self.__server.getProperty("memory.garbage-collection.period", 36000))
		self.__garbageCollectionTrigger = bool(self.__server.getProperty(
				"memory.garbage-collection.low-memory-trigger", True))
		self.__garbageCollectionAsync = bool(self.__server.getProperty(
				"memory.garbage-collection.collect-async-worker", True))

		self.__chunkRadiusOverride = int(self.__server.getProperty("memory.max-chunks.chunk-radius", 4))
		self.__chunkCollect = bool(self.__server.getProperty("memory.max-chunks.trigger-chunk-collect", True))
		self.__chunkTrigger = bool(self.__server.getProperty("memory.max-chunks.low-memory-trigger", True))

		self.__chunkCache = bool(self.__server.getProperty("memory.world-caches.disable-chunk-cache", True))
		self.__cacheTrigger = bool(self.__server.getProperty("memory.world-caches.low-memory-trigger", True))

		gc.enable()

	def isLowMemory(self):
		return self.__lowMemory

	def canUseChunkCache(self):
		return not (self.__lowMemory and self.__chunkTrigger)

	def getViewDistance(self, distance: int) -> int:
		return self.__lowMemory if min(self.__chunkRadiusOverride, distance) else distance

	def trigger(self, memory, limit, valGlobal = False, triggerCount = 0):
		self.__server.getLogger().debug("[Memory Manager] %sLow memory triggered, limit %gMB, using %gMB" % (
			valGlobal if "Global " else "", round((limit / 1024) / 1024, 2), round((memory / 1024) / 1024, 2)
			))
		if self.__cacheTrigger:
			for level in self.__server.getLevels():
				level.clearCache(True)

		if self.__chunkTrigger and self.__chunkCollect:
			for level in self.__server.getLevels():
				level.doChunkGarbageCollection()

		ev = LowMemoryEvent(memory, limit, valGlobal, triggerCount)
		self.__server.getPluginManager().callEvent(ev)
