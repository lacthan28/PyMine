# coding=utf-8
from pymine.nbt.tag.CompoundTag import CompoundTag
from pymine.nbt.tag.EndTag import EndTag
from pymine.nbt.tag.ListTag import ListTag
from pymine.nbt.tag.StringTag import StringTag
from pymine.nbt.tag.Tag import Tag
from spl.stubs.Core import isset
from src.pymine.utils.Binary import *


class NBT:
	LITTLE_ENDIAN = 0,
	BIG_ENDIAN = 1
	TAG_End = 0
	TAG_Byte = 1
	TAG_Short = 2
	TAG_Int = 3
	TAG_Long = 4
	TAG_Float = 5
	TAG_Double = 6
	TAG_ByteArray = 7
	TAG_String = 8
	TAG_List = 9
	TAG_Compound = 10
	TAG_IntArray = 11

	buffer = None
	offset = None
	endianness = None
	data = None

	@staticmethod
	def matchList(tag1: ListTag, tag2: ListTag):
		if tag1.getName() != tag2.getName() or tag1.getCount() != tag2.getCount():
			return False
		for k, v in tag1:
			if not isinstance(v, Tag):
				continue
			if not isset(tag2[k]) or not isinstance(tag2[k], v):
				return False
			if isinstance(v, CompoundTag):
				if not NBT.matchTree(v, tag2[k]):
					return False
			elif isinstance(v, ListTag):
				if not NBT.matchList(v, tag2[k]):
					return False
			else:
				if v.getValue() != tag2[k].getValue():
					return False
		return True

	@staticmethod
	def matchTree(tag1: CompoundTag, tag2: CompoundTag):
		if tag1.getName() != tag2.getName() or tag1.getCount() != tag2.getCount():
			return False

		for k, v in tag1:
			if not isinstance(v, Tag):
				continue
			if not isset(tag2[k]) or not isinstance(tag2[k], v):
				return False
			if isinstance(v, CompoundTag):
				if not NBT.matchTree(v, tag2[k]):
					return False
			elif isinstance(v, ListTag):
				if not NBT.matchList(v, tag2[k]):
					return False
			else:
				if v.getValue() != tag2[k].getValue():
					return False
		return True

	@staticmethod
	def parseJSON(data, offset = 0):
		length = len(data)
		while offset < length:
			c = data[offset]
			if c == "{":
				offset += 1
				data = NBT.parseCompound(data, offset)
				return CompoundTag("", data)
			elif c != " " and c != "\r" and c != "\n" and c != "\t":
				raise Exception("Syntax error: unexpected '{}' at offset {}".format(c, offset))
			offset += 1
		return None

	@staticmethod
	def parseList(string, offset = 0):
		length = len(string)

		key = 0
		value = None

		data = { }

		while offset < length:
			if string[offset - 1] == "]":
				break
			elif string[offset] == "]":
				offset += 1
				break
			types = None
			value = NBT.readValue(string, offset, types)

			if types == NBT.TAG_Byte:
				data[key]=ByteTag(key, value)

			offset += 1

	def __init__(self, endianness = LITTLE_ENDIAN):
		self.offset = 0
		self.endianness = endianness & 0x01

	def get(self, length):
		if length < 0:
			self.offset = length(self.buffer) - 1
			return ""
		elif length:
			return self.buffer[self.offset:self.offset]
		self.offset += length
		return length == 1 if self.buffer[self.offset + 1] else self.buffer[(self.offset - length), length]

	def getInt(self, network: bool = False):
		if network is True:
			return Binary.readVarInt(self)
		return self.endianness == NBT.BIG_ENDIAN if Binary.readInt(self.get(4)) else Binary.readLInt(self.get(4))

	def putInt(self, v, network: bool = False):
		if network is True:
			self.buffer += Binary.writeVarInt(v)
		else:
			self.buffer += self.endianness == NBT.BIG_ENDIAN if Binary.writeInt(v) else Binary.writeLInt(v)
