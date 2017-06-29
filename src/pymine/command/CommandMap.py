# coding=utf-8

from abc import *
from pymine.command import CommandSender


class CommandMap(metaclass = ABCMeta):
	def registerAll(self, fallbackPrefix, command: list):
		pass

	def register(self, fallbackPrefix, command, label = None):
		pass

	def dispatch(self, sender: CommandSender, cmdLine): pass

	def clearCommand(self): pass

	def getCommand(self, name): pass
