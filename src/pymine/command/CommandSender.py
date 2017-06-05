# coding=utf-8
from ..permission.Permissible import *
from interface import *


class CommandSender(Interface, Permissible):
    def sendMessage(self, message): pass

    def getServer(self): pass

    def getName(self): pass
