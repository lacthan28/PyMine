# -*- coding: utf-8 -*-
from pymine.nbt.NBT import NBT
from pymine.nbt.tag.NamedTag import NamedTag
from pymine.nbt.tag.Tag import Tag
from spl.stubs.Core import ArrayAccess, isset, Countable


class ListTag(NamedTag, ArrayAccess, Countable):
	tagType = None

	def __init__(self, name = '', value = None):
		if value is None:
			value = { }
		self.__name = name
		for k, v in value:
			self[k] = v

	def getValue(self):
		value = { }
		for k, v in self:
			if isinstance(v, Tag):
				value[k] = v

		return value

	def getCount(self):
		count = 0
		for tag in self:
			if isinstance(tag, Tag):
				count += 1

		return count

	def offsetExists(self, offset):
		return isset(self[offset])

	def __getitem__(self, offset):
		if isset(self[offset]) and isinstance(self[offset], Tag):
			if isinstance(self[offset], ArrayAccess):
				return self[offset]
			else:
				return self[offset].getValue()

	def __setitem__(self, offset, value):
		if isinstance(value, Tag):
			self[offset] = value
		elif isinstance(self[offset], Tag):
			self[offset].setValue(value)

	def __delitem__(self, offset):
		del self[offset]

	def __len__(self, mode = 2):
		global i
		for i in range(True):
			if not isset(self[i]):
				return i
			if mode == 1:
				if isinstance(self[i], Countable):
					i += len(self[i])
		return i

	def getType(self):
		return NBT.TAG_List

	def setTagType(self, type):
		self.tagType = type

	def getTagType(self):
		return self.tagType

	def read(self, nbt: NBT, network: bool = False):
		self.value = {}
		self.tagType = nbt.getByte()
		size = nbt.getInt(network)
		i=0
		while i<size and not nbt.feof():
			if self.tagType == NBT.TAG_Byte:
				tag = ByteTag("")
