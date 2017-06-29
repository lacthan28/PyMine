# -*- coding: utf-8 -*-

from .MetadataValue import *


class Metadatable(metaclass = ABCMeta):
	def setMetadata(self, metadataKey, newMetadataValue: MetadataValue):
		"""
		Sets a metadata value in the implementing object's metadata store.
		:param str metadataKey:
		:param MetadataValue newMetadataValue:
		:return: void
		"""

	def getMetadata(self, metadataKey):
		"""
		Returns a list of previously set metadata values from the implementing
		object's metadata store.
		:param str metadataKey:
		:return: MetadataValue[]
		"""

	def hasMetadata(self, metadataKey):
		"""
		Tests to see whether the implementing object contains the given
		metadata value in its metadata store.
		:param str metadataKey:
		:return: bool
		"""

	def removeMetadata(self, metadataKey, owningPlugin: Plugin):
		"""
		Removes the given metadata value from the implementing object's
		metadata store.
		:param str metadataKey:
		:param Plugin owningPlugin:
		:return: void
		"""
