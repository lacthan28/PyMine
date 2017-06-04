from copy import *
from .CommandSender import *
from .ConsoleCommandSender import *
from ..Server import *
from ..command.CommandMap import *
from ..event.TranslationContainer import *
from ..isset import *
from ..str_replace import *
from ..utils.TextFormat import *


class Command:
    """ :type list """
    defaultDataTemplate = None

    """ :param name: str """
    name = None
    """
    :param commandData: list
    """
    commandData = {}

    """ :param    
    string """
    nextLabel = None

    """ :param    
    string """
    label = None

    """
    :var
    string[]
    """
    aliases = []

    """
    :var
    string[]
    """
    activeAliases = []

    """ :param    
    CommandMap """
    commandMap = None

    """ :param    
    string """
    description = ""

    """ :param    
    string """
    usageMessage = None

    """ :param    
    string """
    permissionMessage = None

    """ :param    
    TimingsHandler """
    timings = None

    """
    :param
    string   name
    :param
    string   description
    :param
    string   usageMessage
    :param
    string[] aliases
    """

    def __init__(self, name, description="", usageMessage=None, aliases=None):
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

    def execute(self, sender: CommandSender, commandLabel, args: list):
        pass

    """
    :return string
    """

    def getName(self):
        return self.name

    """
    :return string
    """

    def getPermission(self):
        return isset(self.commandData[int("pyminePermission")]) if self.commandData["pyminePermission"] else None

    """
    :param
    string | null permission
                   """

    def setPermission(self, permission):
        if (permission is not None):
            self.commandData["pyminePermission"] = permission
        else:
            del self.commandData["pyminePermission"]

    """
    * @param CommandSender target
    *
    * @return bool
    """

    def testPermission(self, target: CommandSender):
        if self.testPermissionSilent(target):
            return True

        if (self.permissionMessage == None):
            target.sendMessage(TranslationContainer(TextFormat.R + "%commands.generic.permission"))
        elif (self.permissionMessage is not ""):
            target.sendMessage(str_replace("<permission>", self.getPermission(), self.permissionMessage))

        return False

    """
    :param CommandSender target
    *
    :return bool
    """

    def testPermissionSilent(self, target: CommandSender):
        perm = self.getPermission()
        if (perm is None or perm == ""):
            return True

        for permission in perm.split(";"):
            if target.hasPermission(permission):
                return True

        return False

    """
    :return string
    """

    def getLabel(self):
        return self.label

    def setLabel(self, name):
        self.nextLabel = name
        if not self.isRegistered():
            self.timings = TimingsHandler("** Command: " + name)
            self.label = name

            return True

        return False

    """
    * Registers the command into a Command map
    *
    :param CommandMap commandMap
    *
    :return bool
    """

    def register(self, commandMap: CommandMap):
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

    def broadcastCommandMessage(self, source: CommandSender, message, sendToSource=True):
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
