# -*- coding: utf-8 -*-
from pymine.nbt.NBT import NBT
from pymine.nbt.tag.Tag import Tag


class EndTag(Tag):
	def write(self, nbt: NBT, network: bool = False):
		pass

	def getType(self):
		return NBT.TAG_End

	def read(self, nbt: NBT, network: bool = False): pass
