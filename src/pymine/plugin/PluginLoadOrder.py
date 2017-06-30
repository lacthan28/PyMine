# -*- coding: utf-8 -*-
from abc import ABCMeta


class PluginLoadOrder(metaclass=ABCMeta):
	STARTUP = 0
	"""
	The plugin will be loaded at startup
	"""
	POSTWORLD = 1
	"""
	The plugin will be loaded after the first world has been loaded/created.
	"""