# coding=utf-8

from abc import *
from pymine.command import CommandSender
from pymine.command.Command import Command


class CommandMap(metaclass = ABCMeta):
	def registerAll(self, fallbackPrefix, command: dict):
		pass

	def register(self, fallbackPrefix, command:Command, label = None):
		pass

	def dispatch(self, sender: CommandSender, cmdLine): pass

	def clearCommand(self): pass

	def getCommand(self, name): pass
