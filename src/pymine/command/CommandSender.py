# coding=utf-8
from ..permission.Permissible import *


class CommandSender(metaclass=ABCMeta, Permissible):
    def sendMessage(self, message): pass

    def getServer(self): pass

    def getName(self): pass
