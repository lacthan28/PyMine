# -*- coding: utf-8 -*-
from abc import ABCMeta

from ..command.CommandExecutor import *


class Plugin(metaclass = ABCMeta, CommandExecutor):
	def onLoad(self):
		"""
		Called when the plugin is loaded, before calling onEnable()
		:return:
		"""

	def onEnable(self):
		"""
		Called when the plugin is enabled
		:return:
		"""

	def isEnabled(self):
		pass

	def onDisable(self):
		"""
		Called when the plugin is disabled
		Use this to free open things and finish actions
		:return:
		"""

	def isDisabled(self):
		pass

	def getDataFolder(self):
		"""
		Gets the plugin's data folder to save files and configuration.
		This directory name has a trailing slash.
		:return:
		"""

	def getDescription(self):
		"""
		:rtype: PluginDescription
		:return: PluginDescription
		"""

	def getResource(self, filename):
		"""
		Gets an embedded resource in the plugin file.
		:param str filename:
		:return:
		"""

	def saveResource(self, filename, replace = False):
		"""
		Saves an embedded resource to its relative location in the data folder
		:param str filename:
		:param bool replace:
		:return:
		"""

	def getResources(self):
		"""
		Returns all the resources packaged with the plugin
		:return:
		"""

	def getConfig(self):
		"""

		:return: /pymine/utils/Config
		"""

	def saveConfig(self):
		pass

	def saveDefaultConfig(self):
		pass

	def reloadConfig(self):
		pass

	def getServer(self):
		"""

		:return: /pymine/Server
		"""

	def getName(self):
		pass

	def getLogger(self):
		"""

		:return: PluginLogger
		"""

	def getPluginLoader(self):
		"""

		:return: PluginLoader
		"""
