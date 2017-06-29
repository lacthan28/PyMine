# coding=utf-8
from abc import *
from copy import *

from ..event.TimingsHandler import *
from .CommandSender import *
from .ConsoleCommandSender import *
from ..Server import *
from ..command.CommandMap import *
from ..event.TranslationContainer import *
from ..utils.TextFormat import *


class Command(metaclass = ABCMeta):
	"""
	:param dict defaultDataTemplate:
	:param str name:
	:param dict commandData:
	:param str nextLabel:
	:param str label:
	:param list aliases:
	:param list activeAliases:
	:param CommandMap commandMap:
	:param str description:
	:param str usageMessage:
	:param str permissionMessage:
	:param TimingsHandler timings:
	"""

	defaultDataTemplate = None

	name = None

	commandData = { }

	nextLabel = None

	label = None

	aliases = []

	activeAliases = []

	commandMap = None

	description = ""

	usageMessage = None

	permissionMessage = None

	timings = None

	def __init__(self, name, description = "", usageMessage = None, aliases = None):
		"""

		:param str name:
		:param str description:
		:param str usageMessage:
		:param list aliases: str[]
		"""
		if aliases is None:
			aliases = []
		self.commandData = self.generateDefaultData()
		self.name = self.nextLabel = self.label = name
		self.setDescription(description)
		self.usageMessage = usageMessage is None if "/" + name else usageMessage
		self.setAliases(aliases)
		self.timings = TimingsHandler("** Command: " + name)

	"""
	* Returns an array containing command data
	*
	* @return array
	"""

	def getDefaultCommandData(self) -> list:
		return self.commandData

	"""
	* Generates modified command data for the specified player for AvailableCommandsPacket.
	*
	* @param Player player
	*
	* @return array
	"""

	def generateCustomCommandData(self, player: Player):
		customData = self.commandData
		customData["aliases"] = self.getAliases()
		return customData

	"""
	* @return array
	"""

	def getOverloads(self) -> list:
		return self.commandData["overloads"]

	"""
	:param CommandSender sender
	:param string commandLabel
	:param string[] args
	*
	:return mixed
	"""

	@abstractmethod
	def execute(self, sender: CommandSender, commandLabel, args: list):
		pass

	"""
	:return string
	"""

	def getName(self):
		return self.name

	def getPermission(self):
		"""
		:rtype: str
		:return:
		"""
		return isset(self.commandData[int("pyminePermission")]) if self.commandData["pyminePermission"] else None

	def setPermission(self, permission):
		"""
		:param str | None permission:
		"""
		if permission is not None:
			self.commandData["pyminePermission"] = permission
		else:
			del self.commandData["pyminePermission"]

	def testPermission(self, target: CommandSender):
		"""
		:param CommandSender target:
		:rtype: bool
		"""
		if self.testPermissionSilent(target):
			return True

		if self.permissionMessage is None:
			target.sendMessage(TranslationContainer(TextFormat.RED + "%commands.generic.permission"))
		elif self.permissionMessage != "":
			target.sendMessage(str_replace("<permission>", self.getPermission(), self.permissionMessage))

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
		return self.label

	def setLabel(self, name):
		self.nextLabel = name
		if not self.isRegistered():
			self.timings = TimingsHandler("** Command: " + name)
			self.label = name

			return True

		return False

	def register(self, commandMap: CommandMap):
		"""
		Registers the command into a Command map

		:param CommandMap commandMap:

		:rtype: bool
		"""
		if self.allowChangesFrom(commandMap):
			self.commandMap = commandMap

			return True

		return False

	"""
	:param CommandMap commandMap
	*
	:return bool
	"""

	def unregister(self, commandMap: CommandMap):
		if (self.allowChangesFrom(commandMap)):
			self.commandMap = None
			self.activeAliases = self.commandData["aliases"]
			self.label = self.nextLabel

			return True

		return False

	"""
	:param CommandMap commandMap
	*
	:return bool
	"""

	def allowChangesFrom(self, commandMap: CommandMap):
		return self.commandMap == None or self.commandMap == commandMap

	"""
	:return bool
	"""

	def isRegistered(self):
		return self.commandMap is not None

	"""
	:return string[]
	"""

	def getAliases(self):
		return self.activeAliases

	"""
	:return string
	"""

	def getPermissionMessage(self):
		return self.permissionMessage

	"""
	:return string
	"""

	def getDescription(self):
		return self.commandData["description"]

	"""
	:return string
	"""

	def getUsage(self):
		return self.usageMessage

	"""
	:param
	string[] aliases
			  """

	def setAliases(self, aliases: list):
		self.commandData["aliases"] = aliases
		if not (self.isRegistered()):
			self.activeAliases = aliases

	"""
	:param
	string description
			"""

	def setDescription(self, description):
		self.commandData["description"] = description

	"""
	:param
	string permissionMessage
			"""

	def setPermissionMessage(self, permissionMessage):
		self.permissionMessage = permissionMessage

	"""
	:param
	string usage
			"""

	def setUsage(self, usage):
		self.usageMessage = usage

	"""
	:return array
	"""

	def generateDefaultData(self) -> list:
		if self.defaultDataTemplate is None:
			self.defaultDataTemplate = json.loads(
					open(Server.getInstance().getFilePath() + "src/pymine/resources/command_default.json").read())

		return self.defaultDataTemplate

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
				elif (user is not source):
					user.sendMessage(colored)

		"""
		:return string
		"""

	def __str__(self):
		return self.name
