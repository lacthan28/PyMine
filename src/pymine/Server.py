# coding=utf-8
from random import randint

import time
import sys, getopt
import math
from threading import Thread
from os import mkdir
import base64

from pymine.command.CommandReader import CommandReader
from pymine.command.PluginIdentifiableCommand import PluginIdentifiableCommand
from pymine.entity.Entity import Entity
from pymine.event.level.LevelInitEvent import LevelInitEvent
from pymine.event.level.LevelLoadEvent import LevelLoadEvent
from pymine.lang.BaseLang import BaseLang
from pymine.level.Level import *
from pymine.level.LevelException import LevelException
from pymine.level.format.io.LevelProviderManager import LevelProviderManager
from pymine.level.generator.Generator import Generator
from pymine.nbt.NBT import NBT
from pymine.nbt.tag.ByteTag import ByteTag
from pymine.nbt.tag.CompoundTag import CompoundTag
from pymine.nbt.tag.DoubleTag import DoubleTag
from pymine.nbt.tag.FloatTag import FloatTag
from pymine.nbt.tag.IntTag import IntTag
from pymine.nbt.tag.ListTag import ListTag
from pymine.nbt.tag.LongTag import LongTag
from pymine.nbt.tag.ShortTag import ShortTag
from pymine.nbt.tag.StringTag import StringTag
from pymine.scheduler.FileWriteTask import FileWriteTask
from pymine.utils.Config import Config
from pymine.utils.VersionString import VersionString
from spl.ClassLoader import ClassLoader
from spl.ThreadedLogger import ThreadedLogger
from .OfflinePlayer import *
from .Player import *
from .PyMine import *
from .inventory.Recipe import *


class Server:
	DIRECTORY_SEPARATOR = "/"
	BROADCAST_CHANNEL_ADMINISTRATIVE = "pymine.broadcast.admin"
	BROADCAST_CHANNEL_USERS = "pymine.broadcast.user"

	# @var Server
	instance = None

	# @var \Threaded
	sleeper = None

	# @var BanList
	banByName = None

	# @var BanList
	banByIP = None

	# @var Config
	operators = None

	# @var Config
	whitelist = None

	# @var bool
	varIsRunning = True

	hasStopped = False

	# @var PluginManager
	pluginManager = None

	profilingTickRate = 20

	# @var AutoUpdater
	updater = None

	# @var ServerScheduler
	scheduler = None

	# ==========================================================================
	# Counts the ticks since the server start
	#
	# @var int
	# ==========================================================================

	tickCounter = None
	nextTick = 0
	tickAverage = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
	useAverage = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	currentTPS = 20
	currentUse = 0

	# @var bool
	doTitleTick = True

	sendUsageTicker = 0

	dispatchSignals = False

	# @var \AttachableThreadedLogger
	logger = None

	# @var MemoryManager
	memoryManager = None

	# @var CommandReader
	console = None

	# @var SimpleCommandMap
	commandMap = None

	# @var CraftingManager
	craftingManager = None

	# @var ResourcePackManager
	resourceManager = None

	# @var ConsoleCommandSender
	consoleSender = None

	# @var int
	maxPlayers = None

	# @var bool
	autoSave = None

	# @var RCON
	rcon = None

	# @var EntityMetadataStore
	entityMetadata = None

	# @var PlayerMetadataStore
	playerMetadata = None

	# @var LevelMetadataStore
	levelMetadata = None

	# @var Network
	network = None

	networkCompressionAsync = True
	networkCompressionLevel = 7

	autoTickRate = True
	autoTickRateLimit = 20
	alwaysTickPlayers = False
	baseTickRate = 1

	autoSaveTicker = 0
	autoSaveTicks = 6000

	# @var BaseLang
	baseLang = None

	forceLanguage = False

	serverID = None

	autoloader = None
	filePath = None
	dataPath = None
	pluginPath = None

	uniquePlayers = []

	# @var QueryHandler
	queryHandler = None

	# @var QueryRegenerateEvent
	queryRegenerateTask = None

	# @var Config
	properties = None

	propertyCache = []

	# @var Config
	config = None

	# @var Player[]
	players = []

	# @var Player[]
	playerList = []

	identifiers = []

	# @var Level[]
	levels = {}

	# @var Level
	levelDefault = None

	# ===========================================================================
	# @return string
	# ===========================================================================
	@staticmethod
	def getName():
		return "PyMine-DerivedVersion"

	# ===========================================================================
	# @return bool
	# ===========================================================================
	def isRunning(self):
		return self.varIsRunning == True

	# ===========================================================================
	# @return string
	# ===========================================================================
	@staticmethod
	def getPymineVersion():
		return PyMine.VERSION

	# ===========================================================================
	# @return string
	# ===========================================================================
	@staticmethod
	def getCodename():
		return PyMine.CODENAME

	# ===========================================================================
	# @return string
	# ===========================================================================
	@staticmethod
	def getVersion():
		return PyMine.MINECRAFT_VERSION

	# ===========================================================================
	# @return string
	# ===========================================================================
	@staticmethod
	def getApiVersion():
		return PyMine.API_VERSION

	# ===========================================================================
	# @return string
	# ===========================================================================
	def getFilePath(self):
		return self.filePath

	# ===========================================================================
	# @return string
	# ===========================================================================
	def getDataPath(self):
		return self.dataPath

	# ===========================================================================
	# @return string
	# ===========================================================================
	def getPluginPath(self):
		return self.pluginPath

	# ===========================================================================
	# @return int
	# ===========================================================================
	def getMaxPlayers(self):
		return self.maxPlayers

	# ===========================================================================
	# @return int
	# ===========================================================================
	def getPort(self):
		return self.getConfigInt("server-port", 19132)

	# ===========================================================================
	# @return int
	# ===========================================================================
	def getViewDistance(self) -> int:
		return max(2, self.getConfigInt("view-distance", 8))

	# ===========================================================================
	# Returns a view distance up to the currently-allowed limit.
	#
	# @param int distance
	#
	# @return int
	# ===========================================================================
	def getAllowedViewDistance(self, distance: int) -> int:
		return max(2, min(distance, self.memoryManager.getViewDistance(self.getViewDistance())))

	# ===========================================================================
	# @return string
	# ===========================================================================
	def getIp(self):
		return self.getConfigString("server-ip", "0.0.0.0")

	def getServerUniqueId(self):
		return self.serverID

	# ===========================================================================
	# @return bool
	# ===========================================================================
	def getAutoSave(self):
		return self.autoSave

	# ===========================================================================
	# @param bool value
	# ===========================================================================
	def setAutoSave(self, value):
		self.autoSave = bool(value)
		for level in self.getLevels():
			level.setAutoSave(self.autoSave)

	# ===========================================================================
	# @return string
	# ===========================================================================
	def getLevelType(self):
		return self.getConfigString("level-type", "DEFAULT")

	# ===========================================================================
	# @return bool
	# ===========================================================================
	def getGenerateStructures(self):
		return self.getConfigBoolean("generate-structures", True)

	# ===========================================================================
	# @return int
	# ===========================================================================
	def getGamemode(self):
		return self.getConfigInt("gamemode", 0) & 0b11

	# ===========================================================================
	# @return bool
	# ===========================================================================
	def getForceGamemode(self):
		return self.getConfigBoolean("force-gamemode", False)

	# ===========================================================================
	# Returns the gamemode text name
	#
	# @param int mode
	#
	# @return string
	# ===========================================================================
	@staticmethod
	def getGamemodeString(mode):
		if int(mode) == Player.SURVIVAL:
			return "%gameMode.survival"

		elif int(mode) == Player.CREATIVE:
			return "%gameMode.creative"

		elif int(mode) == Player.ADVENTURE:
			return "%gameMode.adventure"

		elif int(mode) == Player.SPECTATOR:
			return "%gameMode.spectator"

		else:
			return "UNKNOWN"

	# ===========================================================================
	# Parses a string and returns a gamemode integer, -1 if not found
	#
	# @param string str
	#
	# @return int
	# ===========================================================================
	@staticmethod
	def getGamemodeFromString(string):
		kq = string.lower().strip()
		if kq == (str(Player.SURVIVAL) or "survival" or "s"):
			return Player.SURVIVAL

		elif kq == (str(Player.CREATIVE) or "creative" or "c"):
			return Player.CREATIVE

		elif kq == (str(Player.ADVENTURE) or "adventure" or "a"):
			return Player.ADVENTURE

		elif kq == (str(Player.SPECTATOR) or "spectator" or "view" or "v"):
			return Player.SPECTATOR

		else:
			return -1

	# ===========================================================================
	# @param string string
	#
	# @return int
	# ===========================================================================
	@staticmethod
	def getDifficultyFromString(string):
		value = string.lower().strip()
		if value == ("0" or "peaceful" or "p"):
			return 0

		elif value == ("1" or "easy" or "e"):
			return 1

		elif value == ("2" or "normal" or "n"):
			return 2

		elif value == ("3" or "hard" or "h"):
			return 3

		else:
			return -1

	# ===========================================================================
	# @return int
	# ===========================================================================
	def getDifficulty(self):
		return self.getConfigInt("difficulty", 1)

	# ===========================================================================
	# @return bool
	# ===========================================================================
	def hasWhitelist(self):
		return self.getConfigBoolean("white-list", False)

	# ===========================================================================
	# @return int
	# ===========================================================================
	def getSpawnRadius(self):
		return self.getConfigInt("spawn-protection", 16)

	# ===========================================================================
	# @return bool
	# ===========================================================================
	def getAllowFlight(self):
		return self.getConfigBoolean("allow-flight", False)

	# ===========================================================================
	# @return bool
	# ===========================================================================
	def isHardcore(self):
		return self.getConfigBoolean("hardcore", False)

	# ===========================================================================
	# @return int
	# ===========================================================================
	def getDefaultGamemode(self):
		return self.getConfigInt("gamemode", 0) & 0b11

	# ===========================================================================
	# @return string
	# ===========================================================================
	def getMotd(self):
		return self.getConfigString("motd", "Minecraft: PE Server")

	# ===========================================================================
	# @return \ClassLoader
	# ===========================================================================
	def getLoader(self):
		return self.autoloader

	# ===========================================================================
	# @return \AttachableThreadedLogger
	# ===========================================================================
	def getLogger(self):
		return self.logger

	# ===========================================================================
	# @return EntityMetadataStore
	# ===========================================================================
	def getEntityMetadata(self):
		return self.entityMetadata

	# ===========================================================================
	# @return PlayerMetadataStore
	# ===========================================================================
	def getPlayerMetadata(self):
		return self.playerMetadata

	def getLevelMetadata(self):
		"""

		:return: LevelMetadataStore
		"""
		return self.levelMetadata

	def getUpdater(self):
		"""

		:return: AutoUpdater
		"""
		return self.updater

	def getPluginManager(self):
		"""

		:return: PluginManager
		"""
		return self.pluginManager

	def getCraftingManager(self):
		"""

		:return: CraftingManager
		"""
		return self.craftingManager

	# def getResourceManager(self):
	# 	"""
	#
	# 	:return: ResourcePackManager
	# 	"""
	# 	return ResourcePackManager(self.resourceManager)
	def getScheduler(self):
		"""

		:return: ServerScheduler
		"""
		return self.scheduler

	def getTick(self):
		"""

		:return: int
		"""
		return self.tickCounter

	def getTicksPerSecond(self):
		"""
		Returns the last server TPS measure
		:return: float
		"""
		return round(self.currentTPS, 2)

	def getTicksPerSecondAverage(self):
		"""
		Returns the last server TPS average measure
		:return: float
		"""
		return round(sum(self.tickAverage) / len(self.tickAverage), 2)

	def getTickUsage(self):
		"""
		Returns the TPS usage/load in %
		:return: float
		"""
		return round(self.currentUse * 100, 2)

	def getTickUsageAverage(self):
		"""
		Returns the TPS usage/load average in %
		:return: float
		"""
		return round((sum(self.useAverage) / len(self.useAverage)) * 100, 2)

	def getCommandMap(self):
		""" :return: SimpleCommandMap """
		return self.commandMap

	def getOnlinePlayers(self):
		""":return: Player[] """
		return self.playerList

	def addRecipe(self, recipe: Recipe):
		self.craftingManager.registerRecipe(recipe)

	def shouldSavePlayerData(self) -> bool:
		return bool(self.getProperty("player.save-player-data", True))

	def getOfflinePlayer(self, name):
		"""

		:param str name:
		:return: OfflinePlayer|Player
		"""
		name = name.lower()
		result = self.getPlayerExact(name)

		if result is None:
			result = OfflinePlayer(self, name)

		return result

	@staticmethod
	def microtime(get_as_float = False):
		if get_as_float:
			return time.time()
		else:
			return '%f %d' % math.modf(time.time())

	def getOfflinePlayerData(self, name):
		"""

		:param str name:
		:return: CompoundTag
		"""
		name = name.lower()
		path = self.getDataPath() + "players/"
		if self.shouldSavePlayerData():
			if os.path.exists(path + "name.dat"):
				try:
					nbt = NBT(NBT.BIG_ENDIAN)
					nbt.readCompressed(open(path + name + ".dat").read())

					return nbt.getData()
				except:  # zlib decode error / corrupt data
					os.rename(path + "name.dat", path + "name.dat.bak")
					self.logger.notice(self.getLanguage().translateString("pymine.data.playerCorrupted", [name]))

			else:
				self.logger.notice(self.getLanguage().translateString("pymine.data.playerNotFound", [name]))

		spawn = self.getDefaultLevel().getSafeSpawn(self)
		nbt = CompoundTag("", [
			LongTag("firstPlayed", math.floor(self.microtime(True) * 1000)),
			LongTag("lastPlayed", math.floor(self.microtime(True) * 1000)),
			ListTag("Pos", [
				DoubleTag(0, spawn.x),
				DoubleTag(1, spawn.y),
				DoubleTag(2, spawn.z)
				]),
			StringTag("Level", self.getDefaultLevel().getName(self)),
			#             // StringTag("SpawnLevel", self.getDefaultLevel(self).getName(self)),
			#             // IntTag("SpawnX", int(spawn.x),
			#             // IntTag("SpawnY", int(spawn.y),
			#             // IntTag("SpawnZ", int(spawn.z),
			#             // ByteTag("SpawnForced", 1), // TODO
			ListTag("Inventory", []),
			CompoundTag("Achievements", []),
			IntTag("playerGameType", self.getGamemode()),
			ListTag("Motion", [
				DoubleTag(0, 0.0),
				DoubleTag(1, 0.0),
				DoubleTag(2, 0.0)
				]),
			ListTag("Rotation", [
				FloatTag(0, 0.0),
				FloatTag(1, 0.0)
				]),
			FloatTag("FallDistance", 0.0),
			ShortTag("Fire", 0),
			ShortTag("Air", 300),
			ByteTag("OnGround", 1),
			ByteTag("Invulnerable", 0),
			StringTag("NameTag", name),
			])
		nbt.Pos.setTagType(NBT.TAG_Double)
		nbt.Inventory.setTagType(NBT.TAG_Compound)
		nbt.Motion.setTagType(NBT.TAG_Double)
		nbt.Rotation.setTagType(NBT.TAG_Float)

		self.saveOfflinePlayerData(name, nbt)

		return nbt

	def saveOfflinePlayerData(self, name, nbtTag, async = False):
		"""

		:param str name:
		:param CompoundTag nbtTag:
		:param bool async:
		:return:
		"""
		if self.shouldSavePlayerData(self):
			nbt = NBT(NBT.BIG_ENDIAN)
			try:
				nbt.setData(nbtTag)

				if async:
					self.getScheduler(self).scheduleAsyncTask(
							FileWriteTask(self.getDataPath(self) + "players/" + str.lower(name) + ".dat",
							              nbt.writeCompressed(self)))
				else:
					f = open(self.getDataPath() + "players/" + str.lower(name) + ".dat")
					f.write(nbt.writeCompressed())
					f.close()

			except BaseException as e:
				self.logger.critical(
						self.getLanguage().translateString("pymine.data.saveError", [name, e.__str__()]))
				self.logger.logException(e)

	def getPlayer(self, name):
		"""

		:param str name:
		:return: Player
		"""
		found = None
		name = name.lower()
		delta = sys.int_info.__getattribute__('sizeof_digit')
		for player in self.getOnlinePlayers():
			value = player.getName(self).upper().find(name.upper())
			if value == 0:
				curDelta = strlen(player.getName(self)) - len(name)
				if curDelta < delta:
					found = player
					delta = curDelta

				if curDelta == 0:
					break

		return found

	def getPlayerExact(self, name):
		"""

		:param str name:
		:return: Player
		"""
		name = name.lower()
		for player in self.getOnlinePlayers():
			if player.getLowerCaseName(self) == name:
				return player

		return None

	def matchPlayer(self, partialName):
		"""

		:param str partialName:
		:return: Player[]
		"""
		partialName = partialName.lower()
		matchedPlayers = []
		for player in self.getOnlinePlayers():
			value = player.getName(self).upper().find(partialName.upper())
			if player.getLowerCaseName(self) == partialName:
				matchedPlayers = [player]
				break
			elif value is not False:
				self.matchedPlayers = [player]

		return matchedPlayers

	def removePlayer(self, player):
		"""

		:param Player player:
		:return:
		"""
		_hash = hash(player)
		if isset(self.identifiers[_hash]):
			identifier = self.identifiers[_hash]
			del (self.players[identifier])
			del (self.identifiers[_hash])
			return

		for identifier, p in self.players:
			if player == p:
				del (self.players[identifier])
				del (self.identifiers[hash(player)])
				break

	def getLevels(self):
		"""

		:return: Level[]
		"""
		return self.levels

	def getDefaultLevel(self):
		"""

		:return: Level
		"""
		return self.levelDefault

	def setDefaultLevel(self, level):
		"""
		Sets the default level to a different level
		This won't change the level-name property,
		it only affects the server on runtime
		:param Level level:
		:return:
		"""
		if level is None or (self.isLevelLoaded(level.getFolderName(self)) and level is not self.levelDefault):
			self.levelDefault = level

	def isLevelLoaded(self, name):
		"""

		:param str name:
		:return: bool
		"""
		return isinstance(self.getLevelByName(name), Level)

	def getLevel(self, levelId):
		"""

		:param int levelId:
		:return: Level
		"""
		if isset(self.levels[levelId]):
			return self.levels[levelId]

		return None

	def getLevelByName(self, name):
		"""

		:param str name:
		:return: Level
		"""
		for level in self.getLevels():
			if level.getFolderName(self) == name:
				return level

		return None

	def unloadLevel(self, level, forceUnload = False):
		"""

		:param Level level:
		:param bool forceUnload:
		:return: bool
		:raise ValueError
		"""
		if level == self.getDefaultLevel() and not forceUnload:
			raise ValueError("The default level cannot be unloaded while running, please switch levels.")

		if level.unload(forceUnload):
			del (self.levels[level.getId(self)])

			return True

		return False

	def loadLevel(self, name):
		"""
		Loads a level from the data directory
		:param str name:
		:return: bool
		:raise: LevelException
		"""
		if name.strip() == "":
			raise LevelException("Invalid empty level name")

		if self.isLevelLoaded(name):
			return True
		elif not self.isLevelGenerated(name):
			self.logger.notice(self.getLanguage().translateString("pymine.level.notFound", [name]))

			return False

		path = self.getDataPath() + "worlds/" + name + "/"

		provider = LevelProviderManager.getProvider(path)

		if provider == None:
			self.logger.error(
					self.getLanguage().translateString("pymine.level.loadError", [name, "Unknown provider"]))

			return False

		try:
			level = Level(self, name, path, provider)
		except ValueError as e:

			self.logger.error(
					self.getLanguage().translateString("pymine.level.loadError", [name, e.getMessage(self)]))
			self.logger.logException(e)
			return False

		self.levels[level.getId(self)] = level

		level.initLevel(self)

		self.getPluginManager(self).callEvent(LevelLoadEvent(level))

		level.setTickRate(self.baseTickRate)

		return True

	def generateLevel(self, name, seed = None, generator = None, options = None):
		"""
		Generates a level if it does not exists
		:param str name:
		:param int seed:
		:param str generator: Class name that extends pymine\\level\\generator\\Noise
		:param dict options:
		:return: bool
		"""
		global provider
		if options is None:
			options = { }
		if name.strip() == "" or self.isLevelGenerated(name):
			return False

		random_bytes = ''.join(randint(0, 255) for i in range(4))
		seed = seed is None if Binary.readInt(os.urandom(4)) else int(seed)
		if not isset(options["preset"]):
			options["preset"] = self.getConfigString("generator-settings", "")

		if not generator is not None and class_exists(generator) and issubclass(generator, Generator):
			generator = Generator.getGenerator(self.getLevelType())

		if LevelProviderManager.getProviderByName(
				providerName = self.getProperty("level-settings.default-format", "pmanvil")) is None:
			provider = LevelProviderManager.getProviderByName(providerName = "pmanvil")

		try:
			path = self.getDataPath() + "worlds/" + name + "/"
			"""
			 :param LevelProvider provider:
			"""
			provider.generate(path, name, seed, generator, options)

			level = Level(self, name, path, provider)
			self.levels[level.getId()] = level

			level.initLevel()

			level.setTickRate(self.baseTickRate)

		except BaseException as e:
			self.logger.error(
					self.getLanguage().translateString("pymine.level.generateError", [name, e.getMessage()]))
			self.logger.logException(e)
			return False

		self.getPluginManager().callEvent(LevelInitEvent(level))

		self.getPluginManager().callEvent(LevelLoadEvent(level))

		self.getLogger().notice(self.getLanguage().translateString("pymine.level.backgroundGeneration", [name]))

		centerX = level.getSpawnLocation().getX() >> 4
		centerZ = level.getSpawnLocation().getZ() >> 4

		order = []

		for X in range(-3, 4):
			for Z in range(-3, 4):
				distance = X ** 2 + Z ** 2
				chunkX = X + centerX
				chunkZ = Z + centerZ
				index = Level.chunkHash(chunkX, chunkZ)
				order[index] = distance

		asort(order)

		for index, distance in order:
			Level.getXZ(index, chunkX, chunkZ)
			level.populateChunk(chunkX, chunkZ, True)

		return True

	# ===========================================================================
	# @param string name
	#
	# @return bool
	# ===========================================================================
	def isLevelGenerated(self, name):
		if name.strip() == "":
			return False

		path = self.getDataPath() + "worlds/" + name + "/"
		if not isinstance(self.getLevelByName(name), Level):
			if LevelProviderManager.getProvider(path) is None:
				return False

		return True

	# ===========================================================================
	# Searches all levels for the entity with the specified ID.
	# Useful for tracking entities across multiple worlds without needing strong references.
	# @param int        entityId
	# @param Level|null expectedLevel Level to look in first for the target
	#
	# @return Entity|null
	# ===========================================================================
	def findEntity(self, entityId: int, expectedLevel: Level = None):
		levels = self.levels
		if expectedLevel is not None:
			array_unshift(levels, expectedLevel)

		for level in levels:
			assert (not level.isClosed())
			entity = level.getEntity(entityId)
			if isinstance(entity, Entity):
				return entity

		return None

	# ===========================================================================
	# @param string variable
	# @param string defaultValue
	#
	# @return string
	# ===========================================================================
	def getConfigString(self, variable, defaultValue = ""):
		v = getopt.getopt(sys.argv, "", ["variable."])
		if isset(v[variable]):
			return str(v[variable])

		return self.properties.exists(variable) if self.properties.get(variable) else defaultValue

	# ===========================================================================
	# @param string variable
	# @param mixed  defaultValue
	#
	# @return mixed
	# ===========================================================================
	def getProperty(self, variable, defaultValue = None):
		if not variable in self.propertyCache:
			v = getopt.getopt(sys.argv, "", ["variable."])
			if isset(v[variable]):
				self.propertyCache[variable] = v[variable]
			else:
				self.propertyCache[variable] = self.config.getNested(variable)

		return self.propertyCache[variable] is None if defaultValue else self.propertyCache[variable]

	# ===========================================================================
	# @param string variable
	# @param string value
	# ===========================================================================
	def setConfigString(self, variable, value):
		self.properties.set(variable, value)

	# ===========================================================================
	# @param string variable
	# @param int    defaultValue
	#
	# @return int
	# ===========================================================================
	def getConfigInt(self, variable, defaultValue = 0):
		v = getopt.getopt(sys.argv, "", ["variable."])
		if isset(v[variable]):
			return int(v[variable])

		return self.properties.exists(variable) if int(self.properties.get(variable)) else int(defaultValue)

	# ===========================================================================
	# @param string variable
	# @param int    value
	# ===========================================================================

	def setConfigInt(self, variable, value):

		self.properties.set(variable, int(value))

	# ===========================================================================
	# @param string  variable
	# @param boolean defaultValue
	#
	# @return boolean
	# ===========================================================================

	def getConfigBoolean(self, variable, defaultValue = False):

		v = getopt.getopt(sys.argv, "", ["variable."])

		if isset(v[variable]):
			value = v[variable]
		else:
			value = self.properties.exists(variable) if self.properties.get(variable) else defaultValue

		if isinstance(value, bool):
			return value

		if str.lower(value) == "on" or "True" or "1" or "yes":
			return True

		return False

	# ===========================================================================
	# @param string variable
	# @param bool   value
	# ===========================================================================
	def setConfigBool(self, variable, value):
		self.properties.set(variable, value == True if "1" else "0")

	# ===========================================================================
	# @param string name
	#
	# @return PluginIdentifiableCommand
	# ===========================================================================
	def getPluginCommand(self, name):
		command = self.commandMap.getCommand(name)
		if isinstance(command, PluginIdentifiableCommand):
			return command
		else:
			return None

	# ===========================================================================
	# @return BanList
	# ===========================================================================


	def getNameBans(self):
		return self.banByName

	# ===========================================================================
	# @return BanList
	# ===========================================================================
	def getIPBans(self):
		return self.banByIP

	# ===========================================================================
	# @param string name
	# ===========================================================================
	def addOp(self, name):
		self.operators.set(str.lower(name), True)
		player = self.getPlayerExact(name)
		if player is not None:
			player.recalculatePermissions()

		self.operators.save(True)

	# ===========================================================================
	# @param string name
	# ===========================================================================

	def removeOp(self, name):

		self.operators.remove(str.lower(name))
		player = self.getPlayerExact(name)
		if player is not None:
			player.recalculatePermissions()

		self.operators.save()

	# ===========================================================================
	# @param string name
	# ===========================================================================

	def addWhitelist(self, name):

		self.whitelist.set(str.lower(name), True)

		self.whitelist.save(True)

	# ===========================================================================
	# @param string name
	# ===========================================================================
	def removeWhitelist(self, name):
		self.whitelist.remove(str.lower(name))
		self.whitelist.save()

	# ===========================================================================
	# @param string name
	#
	# @return bool
	# ===========================================================================
	def isWhitelisted(self, name):
		return not self.hasWhitelist() or self.operators.exists(name, True) or self.whitelist.exists(name, True)

	# ===========================================================================
	# @param string name
	#
	# @return bool
	# ===========================================================================
	def isOp(self, name):
		return self.operators.exists(name, True)

	# ===========================================================================
	# @return Config
	# ===========================================================================
	def getWhitelisted(self):
		return self.whitelist

	# ===========================================================================
	# @return Config
	# ===========================================================================
	def getOps(self):
		return self.operators

	def reloadWhitelist(self):
		self.whitelist.reload(self)

	# ===========================================================================
	# @return string[]
	# ===========================================================================
	def getCommandAliases(self):
		section = self.getProperty("aliases")
		result = []
		if is_array(section):
			for key, value in section:
				commands = { }
				if is_array(value):
					commands = value
				else:
					commands[""] = value

				result[key] = commands

		return result

	# ===========================================================================
	# @return Server
	# ===========================================================================
	def getInstance(self):
		return self.instance

	def micSleep(self, ms: int):
		Server.sleeper.wait(ms)

	def microSleep(self, microseconds: int):
		ms = None
		Server.sleeper.synchronized(self.micSleep(ms), microseconds)

	# ===========================================================================
	# @param \ClassLoader    autoloader
	# @param \ThreadedLogger logger
	# @param string          filePath
	# @param string          dataPath
	# @param string          pluginPath
	# ===========================================================================
	def __init__(self, autoloader: ClassLoader, logger: ThreadedLogger, filePath, dataPath, pluginPath):
		self.instance = self
		self.sleeper = Thread()
		self.autoloader = autoloader
		self.logger = logger

		try:

			self.filePath = filePath
			if not file_exists(dataPath + "worlds/"):
				mkdir(dataPath + "worlds/", 0o777)

			if not file_exists(dataPath + "players/"):
				mkdir(dataPath + "players/", 0o777)

			if not file_exists(pluginPath):
				mkdir(pluginPath, 0o777)

			self.dataPath = os.path.realpath(dataPath) + Server.DIRECTORY_SEPARATOR
			self.pluginPath = os.path.realpath(pluginPath) + Server.DIRECTORY_SEPARATOR

			self.console = CommandReader()

			version = VersionString(self.getpymineVersion())

			self.logger.info("Loading pymine.yml...")
			if not file_exists(self.dataPath + "pymine.yml"):
				content = file_get_contents(self.filePath + "src/pymine/resources/pymine.yml")
				if version.isDev():
					content = str_replace("preferred-channel: stable", "preferred-channel: beta", content)
				with open(self.dataPath + "pymine.yml", 'w') as f:
					f.write(content)

			self.config = Config(self.dataPath + "pymine.yml", Config.YAML, [])

			self.logger.info("Loading server properties...")
			self.properties = Config(self.dataPath + "server.properties", Config.PROPERTIES, {
				"motd":                         "Minecraft: PE Server",
				"server-port":                  19132,
				"white-list":                   False,
				"announce-player-achievements": True,
				"spawn-protection":             16,
				"max-players":                  20,
				"allow-flight":                 False,
				"spawn-animals":                True,
				"spawn-mobs":                   True,
				"gamemode":                     0,
				"force-gamemode":               False,
				"hardcore":                     False,
				"pvp":                          True,
				"difficulty":                   1,
				"generator-settings":           "",
				"level-name":                   "world",
				"level-seed":                   "",
				"level-type":                   "DEFAULT",
				"enable-query":                 True,
				"enable-rcon":                  False,
				"rcon.password":                substr(base64.encodebytes(os.urandom(20)), 3, 10),
				"auto-save":                    True,
				"view-distance":                8
				})

			self.forceLanguage = self.getProperty("settings.force-language", False)
			self.baseLang = BaseLang(self.getProperty("settings.language", BaseLang.FALLBACK_LANGUAGE))
			self.logger.info(self.getLanguage().translateString("language.selected",
			                                                        [self.getLanguage().getName(self),
			                                                         self.getLanguage().getLang(self)]))

			self.memoryManager = MemoryManager(self)

			self.logger.info(
					self.getLanguage().translateString("pymine.server.start", [TextFormat.AQUA + self.getVersion(
					self) + TextFormat.RESET]))

			if (poolSize=self.getProperty("settings.async-workers", "auto")) == "auto"):
				poolSize = ServerScheduler.WORKERS
			processors = Utils.getCoreCount(self) - 2

			if processors > 0):
			poolSize = max(1, processors)

			ServerScheduler.WORKERS = poolSize

			if self.getProperty("network.batch-threshold", 256) >= 0):
			Network.BATCH_THRESHOLD = int(self.getProperty("network.batch-threshold", 256)
			else:
			Network.BATCH_THRESHOLD = -1

			self.networkCompressionLevel = self.getProperty("network.compression-level", 7)
			self.networkCompressionAsync = self.getProperty("network.async-compression", True)

			self.autoTickRate = (bool)
			self.getProperty("level-settings.auto-tick-rate", True)
			self.autoTickRateLimit = int(self.getProperty("level-settings.auto-tick-rate-limit", 20)
			self.alwaysTickPlayers = int(self.getProperty("level-settings.always-tick-players", False)
			self.baseTickRate = int(self.getProperty("level-settings.base-tick-rate", 1)

			self.doTitleTick = (bool)
			self.getProperty("console.title-tick", True)

			self.scheduler = ServerScheduler(self)

			if self.getConfigBoolean("enable-rcon", False) == True):
			self.rcon = RCON(this,
			                 self.getConfigString("rcon.password", "",
			                                      self.getConfigInt("rcon.port", self.getPort(self)),
			                                      (ip = self.getIp(self)) != "" if ip: "0.0.0.0", self.getConfigInt(
					"rcon.threads", 1), self.getConfigInt("rcon.clients-per-thread", 50))


			self.entityMetadata = EntityMetadataStore(self)
			self.playerMetadata = PlayerMetadataStore(self)
			self.levelMetadata = LevelMetadataStore(self)

			self.operators = Config(self.dataPath + "ops.txt", Config.ENUM)
			self.whitelist = Config(self.dataPath + "white-list.txt", Config.ENUM)
			if file_exists(self.dataPath + "banned.txt") and not file_exists(self.dataPath + "banned-players.txt")):
				@
			rename(self.dataPath + "banned.txt", self.dataPath + "banned-players.txt")

			@touch(self.dataPath + "banned-players.txt")

			self.banByName = BanList(self.dataPath + "banned-players.txt")
			self.banByName.load(self)

			@touch(self.dataPath + "banned-ips.txt")

			self.banByIP = BanList(self.dataPath + "banned-ips.txt")
			self.banByIP.load(self)

			self.maxPlayers = self.getConfigInt("max-players", 20)
			self.setAutoSave(self.getConfigBoolean("auto-save", True))

			if self.getConfigBoolean("hardcore", False) == True and self.getDifficulty(self) < 3):
				self.setConfigInt("difficulty", 3)

			define('pymine\DEBUG', int(self.getProperty("debug.level", 1))

			if (int(ini_get('zend.assertions')) > 0 and ((bool)
			self.getProperty("debug.assertions.warn-if-enabled", True)) != =False):
				self.logger.warning(
						"Debugging assertions are enabled, this may impact on performance. To disable them, set `zend.assertions = -1` in php.ini.")

			ini_set('assert.exception', (bool)
			self.getProperty("debug.assertions.throw-exception", 0))

			if self.logger instanceof MainLogger):
				self.logger.setLogDebug(\pymine\DEBUG > 1)


			if                                                           \pymine\DEBUG >= 0):
				@
			cli_set_process_title(self.getName(self) + " " + self.getpymineVersion(self))

			self.logger.info(self.getLanguage().translateString("pymine.server.networkStart",
			[self.getIp(self) == "" if "*": self.getIp(
					self), self.getPort(self)]))
			define("BOOTUP_RANDOM", random_bytes(16))
			self.serverID = Utils.getMachineUniqueId(self.getIp(self) + self.getPort(self))

			self.getLogger(self).debug("Server unique id: " + self.getServerUniqueId(self))
			self.getLogger(self).debug("Machine unique id: " + Utils.getMachineUniqueId(self))

			self.network = Network(this)
			self.network.setName(self.getMotd(self))

			self.logger.info(self.getLanguage().translateString("pymine.server.info", [
				self.getName(self),
				(version.isDev(self) if TextFormat.YELLOW: "" + version.get(True) + TextFormat.WHITE,
			                                                                                    self.getCodename(self),
			                                                                                    self.getApiVersion(self)
			]))
			self.logger.info(self.getLanguage().translateString("pymine.server.license", [self.getName(self)]))

			Timings.init(self)

			self.consoleSender = ConsoleCommandSender()
			self.commandMap = SimpleCommandMap(this)

			Entity.init(self)
			Tile.init(self)
			InventoryType.init(self)
			Block.init(self)
			Enchantment.init(self)
			Item.init(self)
			Biome.init(self)
			Effect.init(self)
			Attribute.init(self)
			self.craftingManager = CraftingManager(self)

			self.resourceManager = ResourcePackManager(this,
		self.getDataPath(self) + "resource_packs" + DIRECTORY_SEPARATOR)

		self.pluginManager = PluginManager(this, self.commandMap)
		self.pluginManager.subscribeToPermission(Server.BROADCAST_CHANNEL_ADMINISTRATIVE, self.consoleSender)
		self.pluginManager.setUseTimings(self.getProperty("settings.enable-profiling", False))
		self.profilingTickRate = (float)
		self.getProperty("settings.profile-report-trigger", 20)
		self.pluginManager.registerInterface(PharPluginLoader.class )
		self.pluginManager.registerInterface(ScriptPluginLoader.

		class )

		register_shutdown_function([this, "crashDump"])

		self.queryRegenerateTask = QueryRegenerateEvent(this, 5)
		self.network.registerInterface(RakLibInterface(this))

		self.pluginManager.loadPlugins(self.pluginPath)

		self.updater = AutoUpdater(this, self.getProperty("auto-updater.host", "www.pymine.net"))

		self.enablePlugins(PluginLoadOrder.

		STARTUP)

		LevelProviderManager.addProvider(Anvil.class )
		LevelProviderManager.

		addProvider(McRegion.class )
		LevelProviderManager.

		addProvider(PMAnvil.class )
		if extension_loaded("leveldb")):
			self.logger.debug(self.getLanguage().translateString("pymine.debug.enable"))

		LevelProviderManager.addProvider(LevelDB.class )



		Generator.

		addGenerator(Flat.class , "flat")
		Generator.

		addGenerator(Normal.class , "normal")
		Generator.

		addGenerator(Normal.class , "default")
		Generator.

		addGenerator(Nether.class , "hell")
		Generator.

		addGenerator(Nether.class , "nether")

		foreach((array) self.getProperty("worlds", []) as name= > worldSetting):
			if

		self.loadLevel(name) == False):
		seed = self.getProperty("worlds.name.seed", time(self))
		options = explode(":", self.getProperty("worlds.name.generator", Generator.getGenerator("default")))
		generator = Generator.getGenerator(array_shift(options))
		if count(options) > 0):
		options = [
			"preset": implode(":", options),
		]
		else:
		options = []

		self.generateLevel(name, seed, generator, options)

		if self.getDefaultLevel(self) == null):
		default = self.getConfigString("level-name", "world")
		if trim(default) == "":
			self.getLogger(self).warning("level-name cannot be null, using default")
		default = "world"
		self.setConfigString("level-name", "world")

		if self.loadLevel(default) == False):
		seed = getopt(sys.argv, "", ["level-seed."])["level-seed"] ?? self.properties.get("level-seed", time.time())
		if not is_numeric(seed) or bccomp(seed, "9223372036854775807") > 0):
		seed = Utils.javaStringHash(seed)
		elif PHP_INT_SIZE == 8):
		seed = int(seed

		self.generateLevel(default, seed == 0 if time(self): seed)


		self.setDefaultLevel(self.getLevelByName(default))

		self.properties.save(True)

		if not (self.getDefaultLevel(self)
		instanceof
		Level)):
		self.getLogger(self).emergency(self.getLanguage().translateString("pymine.level.defaultError"))
		self.forceShutdown(self)

		return

		if self.getProperty("ticks-per.autosave", 6000) > 0):
			self.autoSaveTicks = int(self.getProperty("ticks-per.autosave", 6000)

		self.enablePlugins(PluginLoadOrder.POSTWORLD)

		self.start(self)

	except:
	self.exceptionHandler(e)


# ===========================================================================
# @param string        message
# @param Player[]|null recipients
#
# @return int
# ===========================================================================


def broadcastMessage(message, recipients = null):
	if not is_array(recipients)):
		return self.broadcast(message, self.BROADCAST_CHANNEL_USERS)


	# =========================================================================== @var Player[] recipients #===========================================================================
	foreach(recipients as recipient):
	recipient.sendMessage(message)


return count(recipients)


# ===========================================================================
# @param string        tip
# @param Player[]|null recipients
#
# @return int
# ===========================================================================
def broadcastTip(tip, recipients = null):
	if not is_array(recipients)):
	# =========================================================================== @var Player[] recipients #===========================================================================
		recipients = []

	foreach(self.pluginManager.getPermissionSubscriptions(self.BROADCAST_CHANNEL_USERS) as permissible):
	if permissible instanceof Player and permissible.hasPermission(self.
	BROADCAST_CHANNEL_USERS)):
	recipients[spl_object_hash(permissible)] = permissible // do
	not send
	messages
	directly, or some
	might
	be
	repeated

	# =========================================================================== @var Player[] recipients #===========================================================================
	foreach(recipients as recipient):
	recipient.sendTip(tip)

	return count(recipients)  # ===========================================================================


# @param string        popup
# @param Player[]|null recipients
#
# @return int
# ===========================================================================
def broadcastPopup(popup, recipients = null):
	if not is_array(recipients)):
	# =========================================================================== @var Player[] recipients #===========================================================================
		recipients = []

	foreach(self.pluginManager.getPermissionSubscriptions(self.BROADCAST_CHANNEL_USERS) as permissible):
	if permissible instanceof Player and permissible.hasPermission(self.
	BROADCAST_CHANNEL_USERS)):
	recipients[spl_object_hash(permissible)] = permissible // do
	not send
	messages
	directly, or some
	might
	be
	repeated

	# =========================================================================== @var Player[] recipients #===========================================================================
	foreach(recipients as recipient):
	recipient.sendPopup(popup)

	return count(recipients)  # ===========================================================================


# @param string message
# @param string permissions
#
# @return int
# ===========================================================================
def broadcast(message, permissions):
	# =========================================================================== @var CommandSender[] recipients #===========================================================================
	recipients = []
	foreach(explode("", permissions) as permission):
	foreach(self.pluginManager.getPermissionSubscriptions(permission) as permissible):
	if permissible instanceof CommandSender and permissible.hasPermission(permission)):
		recipients[spl_object_hash(permissible)] = permissible // do
	not send
	messages
	directly, or some
	might
	be
	repeated

	foreach(recipients as recipient):
	recipient.sendMessage(message)

	return count(recipients)


# ===========================================================================
# Broadcasts a Minecraft packet to a list of players
#
# @param Player[]   players
# @param DataPacket packet


# ===========================================================================
def broadcastPacket(array players, DataPacket


packet):
packet.encode(self)
packet.isEncoded = True
if Network: :
BATCH_THRESHOLD >= 0 and strlen(packet.buffer) >= Network.BATCH_THRESHOLD):
self.batchPackets(players, [packet.buffer], False)
return

foreach(players as player):
player.dataPacket(packet)

if isset(packet.__encapsulatedPacket)):
	unset(packet.__encapsulatedPacket)



	# ===========================================================================
	# Broadcasts a list of packets in a batch to a list of players
	#
	# @param Player[]            players
	# @param DataPacket[]|string packets
	# @param bool                forceSync
	# ===========================================================================


def batchPackets(array players, array


packets, forceSync = False):
Timings.playerNetworkTimer.startTiming(self)
str = ""

foreach(packets as p):
if p instanceof DataPacket):
	if
not p.isEncoded):
p.encode(self)

str + = Binary.writeUnsignedVarInt(strlen(p.buffer)) + p.buffer
else:
str + = Binary.writeUnsignedVarInt(strlen(p)) + p

targets = []
foreach(players as p):
if p.isConnected(self)):
	targets[] = self.identifiers[spl_object_hash(p)]

	if not forceSync and self.networkCompressionAsync):
task = CompressBatchedTask(str, targets, self.networkCompressionLevel)
self.getScheduler(self).scheduleAsyncTask(task)
else:
self.broadcastPacketsCallback(zlib_encode(str, ZLIB_ENCODING_DEFLATE, self.networkCompressionLevel), targets)

Timings.playerNetworkTimer.stopTiming(self)


def broadcastPacketsCallback(data, array identifiers

):
pk = BatchPacket(self)
pk.payload = data
pk.encode(self)
pk.isEncoded = True

foreach(identifiers as i):
if isset(self.players[i])):
	self.players[i].dataPacket(pk)





	# ===========================================================================
	# @param int type
	# ===========================================================================


def enablePlugins(type):
	foreach(self.pluginManager.getPlugins(self) as plugin):
	if not plugin.isEnabled(self) and plugin.getDescription(self).getOrder(self) == type):
		self.enablePlugin(plugin)

	if type == PluginLoadOrder: :
	POSTWORLD):
	self.commandMap.registerServerAliases(self)
	DefaultPermissions.registerCorePermissions(self)



	# ===========================================================================
	# @param Plugin plugin
	# ===========================================================================

	def enablePlugin(Plugin plugin

	):
	self.pluginManager.enablePlugin(plugin)

	def disablePlugins(self):
		self.pluginManager.disablePlugins(self)

	def checkConsole(self):
		Timings.serverCommandTimer.startTiming(self)
		line = self.console.getLine(self)
		if line is not None:
			self.pluginManager.callEvent(ev = ServerCommandEvent(self.consoleSender, line))
			if not ev.isCancelled(self):
				self.dispatchCommand(ev.getSender(self), ev.getCommand(self))

		Timings.serverCommandTimer.stopTiming(self)

	# ===========================================================================
	# Executes a command from a CommandSender
	#
	# @param CommandSender sender
	# @param string        commandLine
	#
	# @return bool
	# ===========================================================================
	def dispatchCommand(CommandSender sender, commandLine

	):
	if self.commandMap.dispatch(sender, commandLine)):
		return True

	sender.sendMessage(TranslationContainer(TextFormat.GOLD + "%commands.generic.notFound"))

	return False

	def reload(self):
		self.logger.info("Saving levels...")

		foreach(self.levels as level):
		level.save(self)

	self.pluginManager.disablePlugins(self)
	self.pluginManager.clearPlugins(self)
	self.commandMap.clearCommands(self)

	self.logger.info("Reloading properties...")
	self.properties.reload(self)
	self.maxPlayers = self.getConfigInt("max-players", 20)

	if self.getConfigBoolean("hardcore", False) == True and self.getDifficulty(self) < 3):
		self.setConfigInt("difficulty", 3)

	self.banByIP.load(self)
	self.banByName.load(self)
	self.reloadWhitelist(self)
	self.operators.reload(self)

	foreach(self.getIPBans(self).getEntries(self) as entry):
	self.getNetwork(self).blockAddress(entry.getName(self), -1)

	self.pluginManager.registerInterface(PharPluginLoader.class )
	self.pluginManager.registerInterface(ScriptPluginLoader.

	class )
	self.pluginManager.loadPlugins(self.pluginPath)
	self.enablePlugins(PluginLoadOrder.

	STARTUP)
	self.enablePlugins(PluginLoadOrder.POSTWORLD)
	TimingsHandler.reload(self)


	# ===========================================================================
	# Shutdowns the server correctly
	# ===========================================================================

	def shutdown(self):
		self.isRunning = False

	def forceShutdown(self):
		if self.hasStopped):
			return

		try:
			if not self.isRunning(self)):
				self.sendUsage(SendUsageTask.TYPE_CLOSE)


			self.hasStopped = True

			self.shutdown(self)
			if self.rcon
			instanceof
			RCON):
			self.rcon.stop(self)

			if self.getProperty("network.upnp-forwarding", False) == True):
			self.logger.info("[UPnP] Removing port forward...")
			UPnP.RemovePortForward(self.getPort(self))

			if self.pluginManager
			instanceof
			PluginManager):
			self.getLogger(self).debug("Disabling all plugins")
			self.pluginManager.disablePlugins(self)

			foreach(self.players as player):
			player.close(player.getLeaveMessage(self),
			             self.getProperty("settings.shutdown-message", "Server closed"))

			self.getLogger(self).debug("Unloading all levels")
			foreach(self.getLevels(self) as level):
			self.unloadLevel(level, True)

			self.getLogger(self).debug("Removing event handlers")
			HandlerList.unregisterAll(self)

			self.getLogger(self).debug("Stopping all tasks")
			self.scheduler.cancelAllTasks(self)
			self.scheduler.mainThreadHeartbeat(PHP_INT_MAX)

			self.getLogger(self).debug("Saving properties")
			self.properties.save(self)

			self.getLogger(self).debug("Closing console")
			self.console.shutdown(self)
			self.console.notify(self)

			self.getLogger(self).debug("Stopping network interfaces")
			foreach(self.network.getInterfaces(self) as interface):
			interface.shutdown(self)
			self.network.unregisterInterface(interface)

			gc_collect_cycles(self)
		except:
			self.logger.logException(e)
			self.logger.emergency("Crashed while crashing, killing process")

			@kill(getmypid(self))

	def getQueryInformation(self):
		return self.queryRegenerateTask

	# ===========================================================================
	# Starts the PyMine server and starts processing ticks and packets
	# ===========================================================================
	def start(self):
		if self.getConfigBoolean("enable-query", True) == True):
			self.queryHandler = QueryHandler(self)

		foreach(self.getIPBans(self).getEntries(self) as entry):
		self.network.blockAddress(entry.getName(self), -1)

		if self.getProperty("settings.send-usage", True)):
		self.sendUsageTicker = 6000
		self.sendUsage(SendUsageTask.TYPE_OPEN)



		if self.getProperty("network.upnp-forwarding", False) == True):
			self.logger.info("[UPnP] Trying to port forward...")
		UPnP.PortForward(self.getPort(self))

		self.tickCounter = 0

		if function_exists("pcntl_signal")):
		pcntl_signal(SIGTERM, [this, "handleSignal"])
		pcntl_signal(SIGINT, [this, "handleSignal"])
		pcntl_signal(SIGHUP, [this, "handleSignal"])
		self.dispatchSignals = True

		self.logger.info(self.getLanguage().translateString("pymine.server.defaultGameMode", [self).getGamemodeString(
		self.getGamemode(self))]))

		self.logger.info(self.getLanguage().translateString("pymine.server.startFinished",
		                                                        [round(microtime(True) -)
		 \pymine\START_TIME, 3)]))

		self.tickProcessor(self)
		self.forceShutdown(self)

		def handleSignal(signo):

			if signo == SIGTERM or signo == SIGINT or signo == SIGHUP):
				self.shutdown(self)

		def exceptionHandler(\Throwable e, trace = null):

			if e == null):
				return

	global lastError

	if trace == null):
		trace = e.getTrace(self)

	errstr = e.getMessage(self)
	errfile = e.getFile(self)
	errno = e.getCode(self)
	errline = e.getLine(self)

	type = (errno == E_ERROR or errno == E_USER_ERROR) if \LogLevel.ERROR: (
	(errno == E_USER_WARNING or errno == E_WARNING) if \LogLevel.WARNING: \LogLevel.NOTICE)

	errstr = preg_replace('/\s+/', ' ', trim(errstr))

	errfile = cleanPath(errfile)

	self.logger.logException(e, trace)

	lastError = [
	"type": type,
	"message": errstr,
	"fullFile": e.getFile(self),
	"file": errfile,
	"line": errline,
	"trace": getTrace(0, trace)

	]

	global lastExceptionError, lastError
	lastExceptionError = lastError
	self.crashDump(self)

	def crashDump(self):
		if self.isRunning == False):
			return

	if self.sendUsageTicker > 0):
		self.sendUsage(SendUsageTask.TYPE_CLOSE)

	self.hasStopped = False

	ini_set("error_reporting", 0)
	ini_set("memory_limit", -1) // Fix
	error
	dump
	not dumped
	on
	memory
	problems
	self.logger.emergency(self.getLanguage().translateString("pymine.crash.create"))
	try:
		dump = CrashDump(this)
	except:
		self.logger.logException(e)
		self.logger.critical(self.getLanguage().translateString("pymine.crash.error", [e.getMessage(self)]))
		return

	self.logger.emergency(self.getLanguage().translateString("pymine.crash.submit", [dump.getPath(self)]))

	if self.getProperty("auto-report.enabled", True) is not False):
		report = True
	plugin = dump.getData(self)["plugin"]
	if is_string(plugin)):
	p = self.pluginManager.getPlugin(plugin)
	if p
	instanceof
	Plugin and not (p.getPluginLoader(self)
	instanceof
	PharPluginLoader)):
	report = False

	elif                                                           \Phar.running(True) == "":
	report = False

	if dump.getData(self)["error"]["type"] == "E_PARSE" or dump.getData(self)["error"][
		                                                       "type"] == "E_COMPILE_ERROR"):
	report = False

	if report):
	reply = Utils.postURL("http://" + self.getProperty("auto-report.host", "crash.pymine.net") + "/submit/api", [
		"report": "yes",
	"name": self.getName(self) + " " + self.getpymineVersion(self),
	"email": "crash@pymine.net",
	"reportPaste": base64_encode(dump.getEncodedData(self))
	])

	if (data=json_decode(reply)) is not False and isset(data.crashId)):
		reportId = data.crashId
	reportUrl = data.crashUrl
	self.logger.emergency(self.getLanguage().translateString("pymine.crash.archive", [reportUrl, reportId]))

	// self.checkMemory(self)
	// dump + = "Memory Usage Tracking: \r\n" + chunk_split(
			base64_encode(gzdeflate(implode("", self.memoryStats), 9))) + "\r\n"

	self.forceShutdown(self)
	self.isRunning = False
	                 @ kill(getmypid(self))
	exit(1)

	def __debugInfo(self):
		return []

	private
	function
	tickProcessor(self):
	self.nextTick = microtime(True)
	while (self.isRunning):
		self.tick(self)
		next = self.nextTick - 0.0001
		if next > microtime(True)):
			try:
				@time_sleep_until(next)
			except:
				// Sometimes
				next is less
				than
				the
				current
				time.High
				load?


				def onPlayerLogin(Player player

				):
				if self.sendUsageTicker > 0):
					self.uniquePlayers[player.getRawUniqueId(self)] = player.getRawUniqueId(self)

				self.sendFullPlayerListData(player)
				player.dataPacket(self.craftingManager.getCraftingDataPacket(self))

				def addPlayer(identifier, Player player

				):
				self.players[identifier] = player
				self.identifiers[spl_object_hash(player)] = identifier

				def addOnlinePlayer(Player player

				):
				self.playerList[player.getRawUniqueId(self)] = player

				self.updatePlayerListData(player.getUniqueId(self), player.getId(self), player.getDisplayName(self),
				                          player.getSkinId(self), player.getSkinData(self))

				def removeOnlinePlayer(Player player

				):
				if isset(self.playerList[player.getRawUniqueId(self)])):
					unset(self.playerList[player.getRawUniqueId(self)])

				pk = PlayerListPacket(self)
				pk.type = PlayerListPacket.TYPE_REMOVE
				pk.entries[] = [player.getUniqueId(self)]
				self.broadcastPacket(self.playerList, pk)

				def updatePlayerListData(UUID uuid, entityId, name, skinId, skinData, array

				players = null):
				pk = PlayerListPacket(self)
				pk.type = PlayerListPacket.TYPE_ADD
				pk.entries[] = [uuid, entityId, name, skinId, skinData]
				self.broadcastPacket(players == null if self.playerList: players, pk)


				def removePlayerListData(UUID uuid, array

				players = null):
				pk = PlayerListPacket(self)
				pk.type = PlayerListPacket.TYPE_REMOVE
				pk.entries[] = [uuid]
				self.broadcastPacket(players == null if self.playerList: players, pk)


				def sendFullPlayerListData(Player p

				):
				pk = PlayerListPacket(self)
				pk.type = PlayerListPacket.TYPE_ADD
				foreach(self.playerList as player):
				pk.entries[] = [player.getUniqueId(self), player.getId(self), player.getDisplayName(self),
				                player.getSkinId(self),
				                player.getSkinData(self)]

				p.dataPacket(pk)

				private
				function
				checkTickUpdates(currentTick, tickTime):
				foreach(self.players as p):
				if not p.loggedIn and (tickTime - p.creationTime) >= 10):
					p.close("", "Login timeout")
				elif self.alwaysTickPlayers and p.joined):
					p.onUpdate(currentTick)

					// Do
				level
				ticks
				foreach(self.getLevels(self) as level):
				if level.getTickRate(self) > self.baseTickRate and - -level.tickRateCounter > 0):
					continue

				try:
					levelTime = microtime(True)
					level.doTick(currentTick)
					tickMs = (microtime(True) - levelTime)  # 1000
					level.tickRateTime = tickMs

					if self.autoTickRate):
						if
					tickMs < 50 and level.getTickRate(self) > self.baseTickRate):
					level.setTickRate(r = level.getTickRate(self) - 1)
					if r > self.baseTickRate):
					level.tickRateCounter = level.getTickRate(self)

					self.getLogger(self).debug(
						"Raising level \":level->getName(self)\" tick rate to :level->getTickRate(self) ticks")
					elif tickMs >= 50):
					if level.getTickRate(self) == self.baseTickRate):
						level.setTickRate(
								max(self.baseTickRate + 1, min(self.autoTickRateLimit, floor(tickMs / 50))))
					self.getLogger(self).debug(
						sprintf("Level \"%s\" took %gms, setting tick rate to %d ticks", level.getName(self),
						        round(tickMs, 2),
						        level.getTickRate(self)))
					elif (tickMs / level.getTickRate(self)) >= 50 and level.getTickRate(
							self) < self.autoTickRateLimit):
					level.setTickRate(level.getTickRate(self) + 1)
					self.getLogger(self).debug(
						sprintf("Level \"%s\" took %gms, setting tick rate to %d ticks", level.getName(self),
						        round(tickMs, 2),
						        level.getTickRate(self)))

					level.tickRateCounter = level.getTickRate(self)


					except:
					self.logger.critical(self.getLanguage().translateString("pymine.level.tickError",
					                                                            [level.getName(self),
					                                                             e.getMessage(self)]))
					self.logger.logException(e)

				def doAutoSave(self):
					if self.getAutoSave(self)):
						Timings.worldSaveTimer.startTiming(self)
					foreach(self.players as index: player):
					if player.joined):
						player.save(True)
					elif not player.isConnected(self)):
						self.removePlayer(player)

					foreach(self.getLevels(self) as level):
					level.save(False)

					Timings.worldSaveTimer.stopTiming(self)

					def sendUsage(type = SendUsageTask:
						:

					TYPE_STATUS):
					if self.getProperty("anonymous-statistics.enabled", True)):
						self.scheduler.scheduleAsyncTask(SendUsageTask(this, type, self.uniquePlayers))

					self.uniquePlayers = []



					# ===========================================================================
					# @return BaseLang
					# ===========================================================================

					def getLanguage():

						return self.baseLang

				# ===========================================================================
				# @return bool
				# ===========================================================================
				def isLanguageForced(self):
					return self.forceLanguage

				# ===========================================================================
				# @return Network
				# ===========================================================================
				def getNetwork(self):
					return self.network

				# ===========================================================================
				# @return MemoryManager
				# ===========================================================================
				def getMemoryManager(self):
					return self.memoryManager

				private
				function
				titleTick(self):
				d = Utils.getRealMemoryUsage(self)

				u = Utils.getMemoryUsage(True)
				usage = sprintf("%g/%g/%g/%g MB @ %d threads", round((u[0] / 1024) / 1024, 2),
				                round((d[0] / 1024) / 1024, 2),
				                round((u[1] / 1024) / 1024, 2), round((u[2] / 1024) / 1024, 2),
				                Utils.getThreadCount(self))

				echo
				"\x1b]0" + self.getName(self) + " ".
				self.getpymineVersion(self).
				" | Online " + count(self.players) + "/" + self.getMaxPlayers(self).
				" | Memory " + usage.
				" | U " + round(self.network.getUpload(self) / 1024, 2).
				" D " + round(self.network.getDownload(self) / 1024, 2).
				" kB/s | TPS " + self.getTicksPerSecondAverage(self).
				" | Load " + self.getTickUsageAverage(self) + "%\x07"

				self.network.resetStatistics(self)

				# ===========================================================================
				# @param string address
				# @param int    port
				# @param string payload
				#
				# TODO: move this to Network
				# ===========================================================================
				def handlePacket(address, port, payload):
					try:
						if strlen(payload) > 2 and substr(payload, 0,
						                                  2) == "\xfe\xfd" and self.queryHandler instanceof QueryHandler):
							self.queryHandler.handle(address, port, payload)

						except:
						if                                                           \pymine\DEBUG > 1):
							self.logger.logException(e)

						self.getNetwork(self).blockAddress(address, 600)

						// TODO: add
						raw
						packet
						events

						# ===========================================================================
						# Tries to execute a server tick
						# ===========================================================================
						private
						function
						tick(self):
						tickTime = microtime(True)
						if (tickTime - self.nextTick) < -0.025): // Allow
						half
						a
						tick
						of
						diff
						return False

					Timings.serverTickTimer.startTiming(self)

					+ +self.tickCounter

					self.checkConsole(self)

					Timings.connectionTimer.startTiming(self)
					self.network.processInterfaces(self)

					if self.rcon is not None):
						self.rcon.check(self)

					Timings.connectionTimer.stopTiming(self)

					Timings.schedulerTimer.startTiming(self)
					self.scheduler.mainThreadHeartbeat(self.tickCounter)
					Timings.schedulerTimer.stopTiming(self)

					self.checkTickUpdates(self.tickCounter, tickTime)

					foreach(self.players as player):
					player.checkNetwork(self)

					if (self.tickCounter & 0b1111) == 0):
					if self.doTitleTick and Terminal: :
					hasFormattingCodes(self)):
					self.titleTick(self)

					self.currentTPS = 20
					self.currentUse = 0

					if (self.tickCounter & 0b111111111) == 0):
					try:
						self.getPluginManager(self).callEvent(self.queryRegenerateTask = QueryRegenerateEvent(this,
						                                                                                      5))
						if self.queryHandler is not None):
							self.queryHandler.regenerateInfo(self)

						except:
						self.logger.logException(e)

					self.getNetwork(self).updateName(self)

					if self.autoSave and + +self.autoSaveTicker >= self.autoSaveTicks):
						self.autoSaveTicker = 0
					self.doAutoSave(self)

					if self.sendUsageTicker > 0 and - -self.sendUsageTicker == 0):
					self.sendUsageTicker = 6000
					self.sendUsage(SendUsageTask.TYPE_STATUS)


					if (self.tickCounter % 100) == 0):
						foreach(self.levels as level):
					level.clearCache(self)

					if self.getTicksPerSecondAverage(self) < 12):
					self.logger.warning(self.getLanguage().translateString("pymine.server.tickOverload"))

					if self.dispatchSignals and self.tickCounter % 5 == 0):
					pcntl_signal_dispatch(self)

					self.getMemoryManager(self).check(self)

					Timings.serverTickTimer.stopTiming(self)

					now = microtime(True)
					self.currentTPS = min(20, 1 / max(0.001, now - tickTime))
					self.currentUse = min(1, (now - tickTime) / 0.05)

					TimingsHandler.tick(self.currentTPS <= self.profilingTickRate)

					array_shift(self.tickAverage)
					self.tickAverage[] = self.currentTPS
					array_shift(self.useAverage)
					self.useAverage[] = self.currentUse

					if (self.nextTick - tickTime) < -1:
						self.nextTick = tickTime
					else:
						self.nextTick += 0.05

					return True

				# ===========================================================================
				# Called when something attempts to serialize the server instance.
				#
				# @throws \BadMethodCallException because Server instances cannot be serialized
				# ===========================================================================

				def __sleep(self):
					raise BaseException("Cannot serialize Server instance")
