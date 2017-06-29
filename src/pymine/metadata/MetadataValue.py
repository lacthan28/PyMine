# -*- coding: utf-8 -*-

from ..plugin.Plugin import *


class MetadataValue(metaclass = ABCMeta):
	"""
	:param Plugin owningPlugin:
	"""
	owningPlugin = None

	def __init__(self, owningPlugin: Plugin):
		self.owningPlugin = owningPlugin

	def getOwningPlugin(self):
		""" :return: Plugin """
		return self.owningPlugin

	@abstractmethod
	def value(self):
		"""
		Fetches the value of this metadata item.
		:return: mixed
		"""

	@abstractmethod
	def invalidate(self):
		"""
		Invalidates this metadata item, forcing it to recompute when next accessed.
		:return:
		"""
