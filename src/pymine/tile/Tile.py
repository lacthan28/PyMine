# -*- coding: utf-8 -*-
import inspect
from abc import *

from pymine.event.Timings import Timings
from pymine.level.Level import Level
from pymine.level.Position import Position
from pymine.nbt.tag.CompoundTag import CompoundTag
from spl.stubs.Core import isset, microtime


class Tile(metaclass = ABCMeta, Position):
	"""
	:param Chunk
	"""
	BREWING_STAND = "BrewingStand"
	CHEST = "Chest"
	ENCHANT_TABLE = "EnchantTable"
	FLOWER_POT = "FlowerPot"
	FURNACE = "Furnace"
	ITEM_FRAME = "ItemFrame"
	MOB_SPAWNER = "MobSpawner"
	SIGN = "Sign"
	SKULL = "Skull"
	DISPENSER = "Dispenser"
	DROPPER = "Dropper"
	CAULDRON = "Cauldron"
	HOPPER = "Hopper"
	BEACON = "Beacon"
	ENDER_CHEST = "EnderChest"

	titleCount = 1

	knownTiles = { }
	shortNames = { }

	chunk = None
	name = None
	id = None
	attach = None
	metadata = None
	closed = False
	namedtag = None
	lastUpdate = None
	server = None
	timings = None

	tickTimer = None

	def init(self):
		Tile.registerTile(Beacon)
		Tile.registerTile(Chest)
		Tile.registerTile(EnchantTable)
		Tile.registerTile(FlowerPot)
		Tile.registerTile(Furnace)
		Tile.registerTile(ItemFrame)
		Tile.registerTile(Sign)
		Tile.registerTile(Skull)
		Tile.registerTile(Cauldron)
		Tile.registerTile(Hopper)
		Tile.registerTile(EnderChest)

	@staticmethod
	def createTile(type, level: Level, nbt: CompoundTag, *args):
		"""

		:param str type:
		:param Level level:
		:param CompoundTag nbt:
		:param args:
		 :rtype: Tile
		:return:
		"""
		if isset(Tile.knownTiles[type]):
			cls = Tile.knownTiles[type]
			return cls(level, nbt, *args)

		return None

	@classmethod
	def registerTile(cls):
		"""
		:rtype: bool
		:return:
		"""
		classs = cls()
		if isinstance(cls, Tile) and not inspect.isabstract(classs):
			Tile.knownTiles[type(classs).__name__] = cls
			Tile.shortNames[cls] = type(classs).__name__
			return True

		return False

	def getSaveId(self):
		return Tile.shortNames[__class__]

	def __init__(self, level: Level, nbt: CompoundTag):
		self.timings = Timings.getTileEntityTimings(self)

		self.namedtag = nbt
		self.server = level.getServer()
		self.setLevel(level)
		self.chunk = level.getChunk(self.namedtag['x'] >> 4, self.namedtag['z'] >> 4, False)
		assert self.chunk is not None

		self.name = ""
		self.lastUpdate = microtime(True)
		self.id = Tile.titleCount + 1
		self.x = int(self.namedtag['x'])
		self.y = int(self.namedtag['y'])
		self.z = int(self.namedtag['z'])

		self.chunk.addTile(self)
		self.getLevel().addTile(self)
		self.tickTimer = Timings.getTileEntityTimings(self)


	def getId(self):
		return self.id

	def saveNBT(self):
		self.namedtag.id = StringTag()
