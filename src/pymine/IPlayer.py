from .permission.ServerOperator import *


class IPlayer(ServerOperator):
    # :return: bool
    def isOnline(self):
        pass

    # :return: String
    def getName(self):
        pass

    # :return: bool
    def isBanned(self):
        pass

    # :param banned: bool
    def setBanned(self, banned):
        pass

    # :return: bool
    def isWhitelisted(self):
        pass

    # :param value: bool
    def setWhitelisted(self, value):
        pass

    # :return: Player|null
    def getPlayer(self):
        pass

    # :return: int|double
    def getFirstPlayed(self):
        pass

    # :return: int|double
    def getLastPlayed(self):
        pass

    # :return: mixed
    def hasPlayedBefore(self):
        pass
