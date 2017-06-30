# -*- coding: utf-8 -*-
from abc import ABCMeta

from pymine.command.Command import Command
from pymine.command.CommandSender import CommandSender
from spl.stubs.Core import substr


class VanillaCommand(metaclass=ABCMeta, Command):
	MAX_COORD = 30000000
	MIN_COORD = -30000000

	def __init__(self, name, description = "", usageMessage = None, aliases:dict = {}):
		Command.__init__(self, name, description, usageMessage, aliases)

	def getInteger(self, sender:CommandSender, val, valMin=MIN_COORD, valMax= MAX_COORD):
		i = int(val)

		if i<valMin:
			i = valMin
		elif i > valMax:
			i = valMax

		return i

	def getRelativeDouble(self, original, sender:CommandSender, valInput, valMin=MIN_COORD, valMax= MAX_COORD):
		if valInput[0] == '~':
			val = self.getDouble(sender, substr(valInput, 1))
			return original + val

		return self.getDouble(sender, valInput, valMin, valMax)

	def getDouble(self, sender:CommandSender, val, valMin, valMax):
		i = float(val)

		if i<valMin:
			i = valMin
		elif i > valMax:
			i = valMax

		return i

