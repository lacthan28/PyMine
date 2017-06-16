# -*- coding: utf-8 -*-
from abc import *

from pymine.Player import Player
from pymine.entity.Entity import Entity
from pymine.event.plugin.PluginManager import PluginManager
from pymine.scheduler.PluginTask import PluginTask
from pymine.scheduler.TaskHandler import TaskHandler
from spl.stubs.Core import isset
from .TimingsHandler import TimingsHandler


class Timings(metaclass = ABCMeta):
	"""
	:param TimingsHandler fullTickTimer:
	:param TimingsHandler serverTickTimer: 
	:param TimingsHandler memoryManagerTimer: 
	:param TimingsHandler garbageCollectorTimer: 
	:param TimingsHandler playerListTimer:
	:param TimingsHandler playerNetworkTimer:
	:param TimingsHandler playerNetworkReceiveTimer:
	:param TimingsHandler playerChunkOrderTimer:
	:param TimingsHandler playerChunkSendTimer:
	:param TimingsHandler connectionTimer:
	:param TimingsHandler tickablesTimer:
	:param TimingsHandler schedulerTimer:
	:param TimingsHandler chunkIOTickTimer:
	:param TimingsHandler timeUpdateTimer:
	:param TimingsHandler serverCommandTimer:
	:param TimingsHandler worldSaveTimer:
	:param TimingsHandler generationTimer:
	:param TimingsHandler populationTimer:
	:param TimingsHandler generationCallbackTimer:
	:param TimingsHandler permissibleCalculationTimer:
	:param TimingsHandler permissionDefaultTimer:

	:param TimingsHandler entityMoveTimer:
	:param TimingsHandler tickEntityTimer:
	:param TimingsHandler activatedEntityTimer: 
	:param TimingsHandler tickTileEntityTimer:

	:param TimingsHandler timerEntityBaseTick:
	:param TimingsHandler timerLivingEntityBaseTick:
	:param TimingsHandler timerEntityAI:
	:param TimingsHandler timerEntityAICollision:
	:param TimingsHandler timerEntityAIMove:
	:param TimingsHandler timerEntityTickRest:

	:param TimingsHandler schedulerSyncTimer:
	:param TimingsHandler schedulerAsyncTimer: 

	:param TimingsHandler playerCommandTimer:

	:param TimingsHandler craftingDataCacheRebuildTimer:

	:param dict entityTypeTimingMap: TimingsHandler[]
	:param dict tileEntityTypeTimingMap: TimingsHandler[]
	:param dict packetReceiveTimingMap: TimingsHandler[]
	:param dict packetSendTimingMap: TimingsHandler[]
	:param dict pluginTaskTimingMap: TimingsHandler[]
	"""
	fullTickTimer = None
	serverTickTimer = None
	memoryManagerTimer = None
	garbageCollectorTimer = None
	playerListTimer = None
	playerNetworkTimer = None
	playerNetworkReceiveTimer = None
	playerChunkOrderTimer = None
	playerChunkSendTimer = None
	connectionTimer = None
	tickablesTimer = None
	schedulerTimer = None
	chunkIOTickTimer = None
	timeUpdateTimer = None
	serverCommandTimer = None
	worldSaveTimer = None
	generationTimer = None
	populationTimer = None
	generationCallbackTimer = None
	permissibleCalculationTimer = None
	permissionDefaultTimer = None

	entityMoveTimer = None
	tickEntityTimer = None
	activatedEntityTimer = None
	tickTileEntityTimer = None

	timerEntityBaseTick = None
	timerLivingEntityBaseTick = None
	timerEntityAI = None
	timerEntityAICollision = None
	timerEntityAIMove = None
	timerEntityTickRest = None

	schedulerSyncTimer = None
	schedulerAsyncTimer = None

	playerCommandTimer = None

	craftingDataCacheRebuildTimer = None

	entityTypeTimingMap = {}
	tileEntityTypeTimingMap = {}
	packetReceiveTimingMap = {}
	packetSendTimingMap = {}
	pluginTaskTimingMap = {}

	@staticmethod
	def init():
		if isinstance(Timings.serverTickTimer, TimingsHandler):
			return

		Timings.fullTickTimer = TimingsHandler('Full Server Tick')
		Timings.serverTickTimer = TimingsHandler('** Full Server Tick', Timings.fullTickTimer)
		Timings.memoryManagerTimer = TimingsHandler('Memory Manager')
		Timings.garbageCollectorTimer = TimingsHandler('Garbage Collector', Timings.memoryManagerTimer)
		Timings.playerListTimer = TimingsHandler('Player List')
		Timings.playerNetworkTimer = TimingsHandler('Player Network Send')
		Timings.playerNetworkReceiveTimer = TimingsHandler('Player Network Receive')
		Timings.playerChunkOrderTimer = TimingsHandler('Player Order Chunks')
		Timings.playerChunkSendTimer = TimingsHandler('Player Send Chunks')
		Timings.connectionTimer = TimingsHandler('Connection Handler')
		Timings.tickablesTimer = TimingsHandler('Tickables')
		Timings.schedulerTimer = TimingsHandler('Scheduler')
		Timings.chunkIOTickTimer = TimingsHandler('ChunkIOTick')
		Timings.timeUpdateTimer = TimingsHandler('Time Update')
		Timings.serverCommandTimer = TimingsHandler('Server Command')
		Timings.worldSaveTimer = TimingsHandler('World Save')
		Timings.generationTimer = TimingsHandler('World Generation')
		Timings.populationTimer = TimingsHandler('World Population')
		Timings.generationCallbackTimer = TimingsHandler('World Generation Callback')
		Timings.permissibleCalculationTimer = TimingsHandler('Permissible Calculation')
		Timings.permissionDefaultTimer = TimingsHandler('Default Permission Calculation')

		Timings.entityMoveTimer = TimingsHandler('** entityMove')
		Timings.tickEntityTimer = TimingsHandler('** tickEntity')
		Timings.activatedEntityTimer = TimingsHandler('** activatedTickEntity')
		Timings.tickTileEntityTimer = TimingsHandler('** tickTileEntity')

		Timings.timerEntityBaseTick = TimingsHandler('** entityBaseTick')
		Timings.timerLivingEntityBaseTick = TimingsHandler('** livingEntityBaseTick')
		Timings.timerEntityAI = TimingsHandler('** livingEntityAI')
		Timings.timerEntityAICollision = TimingsHandler('** livingEntityAICollision')
		Timings.timerEntityAIMove = TimingsHandler('** livingEntityAIMove')
		Timings.timerEntityTickRest = TimingsHandler('** livingEntityTickRest')

		Timings.schedulerSyncTimer = TimingsHandler('** Scheduler - Sync Tasks', PluginManager.pluginParentTimer)
		Timings.schedulerAsyncTimer = TimingsHandler('** Scheduler - Async Tasks')

		Timings.playerCommandTimer = TimingsHandler('** playerCommand')
		Timings.craftingDataCacheRebuildTimer = TimingsHandler('** craftingDataCacheRebuild')

	@staticmethod
	def getPluginTaskTimings(task: TaskHandler, period):
		"""

		:param TaskHandler task:
		:param period:
		:rtype: TimingsHandler
		:return:
		"""
		ftask = task.getTask()
		if isinstance(ftask, PluginTask) and ftask.getOwner() is not None:
			plugin = ftask.getOwner().getDescription().getFullName()
		elif task.timingName is not None:
			plugin = 'Scheduler'
		else:
			plugin = 'Unknown'

		taskname = task.getTaskName()

		name = 'Task:' + plugin + ' Runnable: ' + taskname

		if period > 0:
			name += '(interval:' + period + ')'
		else:
			name += '(Single)'

		if not isset(Timings.pluginTaskTimingMap[name]):
			Timings.pluginTaskTimingMap[name] = TimingsHandler(name,Timings.schedulerSyncTimer)

		return Timings.pluginTaskTimingMap[name]

	@staticmethod
	def getEntityTimings(entity:Entity):
		"""

		:param Entity entity:
		:rtype: TimingsHandler
		:return: entityTypeTimingMap[entityType]
		"""
		entityType = type(entity).__name__
		if not isset(Timings.entityTypeTimingMap[entityType]):
			if isinstance(entity, Player):
				Timings.entityTypeTimingMap[entityType] = TimingsHandler('** tickEntity - EntityPlayer', Timings.tickEntityTimer)
			else:
				Timings.entityTypeTimingMap[entityType] = TimingsHandler('** tickEntity - ' + entityType, Timings.tickEntityTimer)
		return Timings.entityTypeTimingMap[entityType]

	@staticmethod
	def getTileEntityTimings(tile:Tile):