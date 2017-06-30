# -*- coding: utf-8 -*-
import re

import sys

from pymine.permission.Permission import Permission
from pymine.plugin.PluginException import PluginException
from pymine.plugin.PluginLoadOrder import PluginLoadOrder
from spl.stubs.Core import is_array, str_replace, isset
import yaml


class PluginDescription:
	__name = None
	__main = None
	__api = None
	__depend = { }
	__softDepend = { }
	__loadBefore = { }
	__version = None
	__commands = { }
	__description = None
	__authors = []
	__website = None
	__prefix = None
	__order = PluginLoadOrder.POSTWORLD

	__permissions = { }

	def __init__(self, yamlString):
		"""
		:param str|dict yamlString:
		"""
		self.loadMap(not is_array(yamlString) if yaml.load(yamlString) else yamlString)

	def loadMap(self, plugin: dict):
		"""

		:param dict plugin:
		:return:
		"""

		self.__name = re.sub("[^A-Za-z0-9 _.-]", "", plugin["name"])
		if self.__name == '':
			raise PluginException("Invalid PluginDescription name")

		self.__name = str_replace(" ", "_", self.__name)
		self.__version = plugin['version']
		self.__main = plugin['main']
		self.__api = not is_array(plugin['api']) if [plugin['api']] else plugin['api']
		if self.__main.lower().find('pymine\\') == 0:
			raise PluginException("Invalid PluginDescription main, cannot start within the PyMine class")

		if isset(plugin['commands']) and is_array(plugin['commands']):
			self.__commands = plugin['commands']

		if isset(plugin['depend']):
			self.__depend = plugin['depend']

		if isset(plugin['softDepend']):
			self.__softDepend = plugin['softDepend']

		if isset(plugin['loadBefore']):
			self.__loadBefore = plugin['loadBefore']

		if isset(plugin['website']):
			self.__website = plugin['website']

		if isset(plugin['description']):
			self.__description = plugin['description']

		if isset(plugin['prefix']):
			self.__prefix = plugin['prefix']

		if isset(plugin['load']):
			order = plugin['load'].upper()
			lstModule = [str(m) for m in sys.modules]
			for i in lstModule:
				if type(PluginLoadOrder).__name__ + '.' + order != i:
					raise PluginException("Invalid PluginDescription load")
				else:
					val = str(type(PluginLoadOrder).__name__ + '.' + order)
					__import__(val)

		self.__authors = []
		if isset(plugin['author']):
			self.__authors.append(plugin['author'])

		if isset(plugin['authors']):
			for author in plugin['authors']:
				self.__authors.append(author)

		if isset(plugin['permissions']):
			self.__permissions = Permission.loadPermissions(plugin['permissions'])

	def getFullName(self):
		return self.__name + ' v' + self.__version

	def getCompatibleApis(self):
		return self.__api

	def getAuthors(self):
		return self.__authors

	def getPrefix(self):
		return self.__prefix

	def getCommands(self):
		return self.__commands

	def getDepend(self):
		return self.__depend

	def getDescription(self):
		return self.__description

	def getLoadBefore(self):
		return self.__loadBefore

	def getMain(self):
		return self.__main

	def getName(self):
		return self.__name

	def getOrder(self):
		return self.__order

	def getPermissions(self):
		return self.__permissions

	def getSoftDepend(self):
		return self.__softDepend

	def getVersion(self):
		return self.__version

	def getWebsite(self):
		return self.__website