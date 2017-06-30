# coding=utf-8
from pymine.event.TextContainer import TextContainer
from .CommandSender import *
from .ConsoleCommandSender import *
from ..Server import *
from ..command.CommandMap import *
from ..event.TimingsHandler import *
from ..event.TranslationContainer import *
from ..utils.TextFormat import *
from copy import copy


class Command(metaclass = ABCMeta):
	"""
	:param dict __defaultDataTemplate:
	:param str __name:
	:param dict _commandData:
	:param str __nextLabel:
	:param str __label:
	:param dict __aliases:
	:param dict __activeAliases:
	:param CommandMap __commandMap:
	:param str _description:
	:param str _usageMessage:
	:param str __permissionMessage:
	:param TimingsHandler timings:
	"""

	__defaultDataTemplate = None
	__name = None
	_commandData = { }
	__nextLabel = None
	__label = None
	__aliases = {}
	__activeAliases = {}
	__commandMap = None
	_description = ""
	_usageMessage = None
	__permissionMessage = None
	timings = None

	def __init__(self, name, description = "", usageMessage = None, aliases:dict = {}):
		"""

		:param str name:
		:param str description:
		:param str usageMessage:
		:param dict aliases: str[]
		"""
		self._commandData = self.generateDefaultData()
		self.__name = self.__nextLabel = self.__label = name
		self.setDescription(description)
		self._usageMessage = usageMessage is None if "/" + name else usageMessage
		self.setAliases(aliases)
		self.timings = TimingsHandler("** Command: " + name)

	def getDefaultCommandData(self) -> dict:
		"""
		* Returns an array containing command data
		*
		* :return: dict
		"""
		return self._commandData

	def generateCustomCommandData(self, player: Player):
		"""
			* Generates modified command data for the specified player for AvailableCommandsPacket.
			*
			* :param Player player:
			*
			* :return: dict
			"""
		customData = self._commandData
		customData["aliases"] = self.getAliases()
		for overloadName, overload in customData['overloads']:
			if isset(overload['pyminePermission']) and not player.hasPermission(overload['pyminePermission']):
				del customData['overloads'][overloadName]
		return customData

	def getOverloads(self) -> dict:
		return self._commandData["overloads"]



	@abstractmethod
	def execute(self, sender: CommandSender, commandLabel, args: dict):
		"""
			:param CommandSender sender:
			:param str commandLabel:
			:param dict args:
			:return: mixed
			"""

	def getName(self):
		"""

		:return: str
		"""
		return self.__name

	def getPermission(self):
		"""
		:rtype: str
		:return:
		"""
		return isset(self._commandData[int("pyminePermission")]) if self._commandData["pyminePermission"] else None

	def setPermission(self, permission):
		"""
		:param str | None permission:
		"""
		if permission is not None:
			self._commandData["pyminePermission"] = permission
		else:
			del self._commandData["pyminePermission"]

	def testPermission(self, target: CommandSender):
		"""
		:param CommandSender target:
		:rtype: bool
		"""
		if self.testPermissionSilent(target):
			return True

		if self.__permissionMessage is None:
			target.sendMessage(TranslationContainer(TextFormat.RED + "%commands.generic.permission"))
		elif self.__permissionMessage != "":
			target.sendMessage(str_replace("<permission>", self.getPermission(), self.__permissionMessage))

		return False

	def testPermissionSilent(self, target: CommandSender):
		"""
		:param CommandSender target:
		:rtype: bool
		"""
		perm = self.getPermission()
		if perm is None or perm == "":
			return True

		for permission in perm.split(";"):
			if target.hasPermission(permission):
				return True

		return False

	def getLabel(self):
		"""
		:rtype: string
		:return: label
		"""
		return self.__label

	def setLabel(self, name):
		self.__nextLabel = name
		if not self.isRegistered():
			self.timings = TimingsHandler("** Command: " + name)
			self.__label = name

			return True

		return False

	def register(self, commandMap: CommandMap):
		"""
		Registers the command into a Command map

		:param CommandMap commandMap:

		:rtype: bool
		"""
		if self.allowChangesFrom(commandMap):
			self.__commandMap = commandMap

			return True

		return False

	"""
	:param CommandMap commandMap
	*
	:return bool
	"""

	def unregister(self, commandMap: CommandMap):
		if self.allowChangesFrom(commandMap):
			self.__commandMap = None
			self.__activeAliases = self._commandData["aliases"]
			self.__label = self.__nextLabel

			return True

		return False

	"""
	:param CommandMap commandMap
	*
	:return bool
	"""

	def allowChangesFrom(self, commandMap: CommandMap):
		return self.__commandMap is None or self.__commandMap == commandMap

	"""
	:return bool
	"""

	def isRegistered(self):
		return self.__commandMap is not None

	"""
	:return string[]
	"""

	def getAliases(self):
		return self.__activeAliases

	"""
	:return string
	"""

	def getPermissionMessage(self):
		return self.__permissionMessage

	"""
	:return string
	"""

	def getDescription(self):
		return self._commandData["description"]

	"""
	:return string
	"""

	def getUsage(self):
		return self._usageMessage

	"""
	:param
	string[] aliases
			  """

	def setAliases(self, aliases: dict):
		self._commandData["aliases"] = aliases
		if not (self.isRegistered()):
			self.__activeAliases = aliases

	"""
	:param
	string description
			"""

	def setDescription(self, description):
		self._commandData["description"] = description

	"""
	:param
	string permissionMessage
			"""

	def setPermissionMessage(self, permissionMessage):
		self.__permissionMessage = permissionMessage

	"""
	:param
	string usage
			"""

	def setUsage(self, usage):
		self._usageMessage = usage

	"""
	:return array
	"""

	def generateDefaultData(self) -> dict:
		if self.__defaultDataTemplate is None:
			self.__defaultDataTemplate = json.loads(
					open(Server.getInstance().getFilePath() + "src/pymine/resources/command_default.json").read())

		return self.__defaultDataTemplate

	"""
	:param CommandSender source
	:param string        message
	:param bool          sendToSource
	"""

	def broadcastCommandMessage(self, source: CommandSender, message, sendToSource = True):
		if isinstance(message, TextContainer):
			m = copy(message)
			result = "[" + source.getName() + ": " + (
				source.getServer().getLanguage().get(m.getText()) is not m.getText() if "%" else "") + m.getText() + "]"

			users = source.getServer().getPluginManager().getPermissionSubscriptions(
					Server.BROADCAST_CHANNEL_ADMINISTRATIVE)
			colored = TextFormat.GRAY.TextFormat.ITALIC.result

			m.setText(result)
			result = copy(m)
			m.setText(colored)
			colored = copy(m)
		else:
			users = source.getServer().getPluginManager().getPermissionSubscriptions(
					Server.BROADCAST_CHANNEL_ADMINISTRATIVE)
			result = TranslationContainer("chat.type.admin", [source.getName(), message])
			colored = TranslationContainer(TextFormat.GRAY + TextFormat.ITALIC + "%chat.type.admin",
			                               [source.getName(), message])

		if sendToSource is True and not isinstance(source, ConsoleCommandSender):
			source.sendMessage(message)

		for user in users:
			if isinstance(user, CommandSender):
				if isinstance(user, ConsoleCommandSender):
					user.sendMessage(result)
				elif user != source:
					user.sendMessage(colored)

		"""
		:return string
		"""

	def __str__(self):
		return self.__name
