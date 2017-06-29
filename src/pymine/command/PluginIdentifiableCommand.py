# -*- coding: utf-8 -*-
from abc import ABCMeta


class PluginIdentifiableCommand(metaclass = ABCMeta):
	def getPlugin(self):
		"""

		:return: Plugin
		"""
