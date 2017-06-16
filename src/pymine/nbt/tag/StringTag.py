# -*- coding: utf-8 -*-
from pymine.nbt.NBT import NBT
from pymine.nbt.tag.NamedTag import NamedTag


class StringTag(NamedTag):
	def getType(self):
		return NBT.TAG_String

	def read(self, nbt: NBT, network: bool = False):
		self.value = nbt.getString(network)

	def write(self, nbt: NBT, network: bool = False):
		nbt.putString(self.value, network)
