# -*- coding: utf-8 -*-
from .Command import *
from .CommandSender import *


class CommandExecutor(metaclass = ABCMeta):
	def onCommand(self, sender: CommandSender, command: Command, label, args: list):
		"""

		:param CommandSender sender:
		:param Command command:
		:param str label:
		:param list args:
		:return: bool
		"""
		pass
