# coding=utf-8
from zope.interface.interface import *

from pymine.command import CommandSender


class CommandMap(Interface):
    def registerAll(self, fallbackPrefix, command: list):
        pass

    def register(self, fallbackPrefix, command, label=None):
        pass

    def dispatch(self, sender: CommandSender, cmdLine): pass

    def clearCommand(self): pass

    def getCommand(self, name): pass
