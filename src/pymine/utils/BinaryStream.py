# -*- coding: utf-8 -*-
from pymine.item.Item import Item
from pymine.utils.Binary import Binary
from pymine.utils.UUID import *
from spl.stubs.Core import substr, isset, stdClass


class BinaryStream(stdClass):
	offset = None
	buffer = None

	def __init__(self, buffer = "", offset = 0):
		self.buffer = buffer
		self.offset = offset

	def reset(self):
		self.buffer = ""
		self.offset = 0

	def setBuffer(self, buffer = None, offset = 0):
		self.buffer = buffer
		self.offset = int(offset)

	def getOffset(self):
		return self.offset

	def getBuffer(self):
		return self.buffer

	def get(self, length):
		if length < 0:
			self.offset = len(self.buffer) - 1
		elif length is True:
			string = substr(self.buffer, self.offset)
			self.offset = len(self.buffer)
			return string

		return length == 1 if self.buffer[self.offset + 1] else substr(self.buffer,
		                                                               (self.offset + length) - length, length)

	def put(self, string):
		self.buffer += string

	def getBool(self) -> bool:
		return bool(self.getByte())

	def putBool(self, v):
		self.putByte(bool(v))

	def getLong(self):
		return Binary.readLong(self.get(8))

	def putLong(self, v):
		self.buffer += Binary.writeLong(v)

	def getInt(self):
		return Binary.readInt(self.get(4))

	def putInt(self, v):
		self.buffer += Binary.writeInt(v)

	def getLLong(self):
		return Binary.readLLong(self.get(8))

	def putLLong(self, v):
		self.buffer += Binary.writeLLong(v)

	def getLInt(self):
		return Binary.readLInt(self.get(4))

	def putLInt(self, v):
		self.buffer += Binary.writeLInt(v)

	def getSignedShort(self):
		return Binary.readSignedShort(self.get(2))

	def putShort(self, v):
		self.buffer += Binary.writeShort(v)

	def getShort(self):
		return Binary.readShort(self.get(2))

	def putSignedShort(self, v):
		self.buffer += Binary.writeShort(v)

	def getFloat(self, accuracy: int = -1):
		return Binary.readFloat(self.get(4), accuracy)

	def putFloat(self, v):
		self.buffer += Binary.writeFloat(v)

	def getLShort(self, signed = True):
		return signed if Binary.readSignedLShort(self.get(2)) else Binary.readLShort(self.get(2))

	def putLShort(self, v):
		self.buffer += Binary.writeLShort(v)

	def getLFloat(self, accuracy: int = -1):
		return Binary.readLFloat(self.get(4), accuracy)

	def putLFloat(self, v):
		self.buffer += Binary.writeLFloat(v)

	def getTriad(self):
		return Binary.readTriad(self.get(3))

	def putTriad(self, v):
		self.buffer += Binary.writeTriad(v)

	def getLTriad(self):
		return Binary.readLTriad(self.get(3))

	def putLTriad(self, v):
		self.buffer += Binary.writeLTriad(v)

	def getByte(self):
		return ord(self.buffer[self.offset + 1])

	def putByte(self, v):
		self.buffer += chr(v)

	def getUUID(self):
		return UUID.fromBinary(self.get(16))

	def putUUID(self, uuid: UUID):
		self.put(uuid.toBinary())

	def getSlot(self):
		id = self.getVarInt()
		if id <= 0:
			return Item.get(0, 0, 0)
		auxValue = self.getVarInt()
		data = auxValue >> 8
		cnt = auxValue & 0xff

		nbtLen = self.getLShort()
		nbt = ''

		if nbtLen > 0:
			nbt = self.get(nbtLen)

		return Item.get(id, data, cnt, nbt)

	def putSlot(self, item: Item):
		if item.getId() == 0:
			self.putVarInt(0)
			return
		self.putVarInt(item.getId())
		auxValue = ((item.getDamage() if item.getDamage() else -1) << 8) | item.getCount()
		self.putVarInt(auxValue)
		nbt = item.getCompoundTag()
		self.putLShort(len(nbt))
		self.put(nbt)

	def getString(self):
		return self.get(self.getUnsignedVarInt())

	def putString(self, v):
		self.putUnsignedVarInt(len(v))
		self.put(v)

	def getVarInt(self):
		return Binary.readVarInt(self)

	def putVarInt(self, v):
		self.put(Binary.writeVarInt(v))

	def getUnsignedVarInt(self):
		return Binary.readUnsignedVarInt(self)

	def putUnsignedVarInt(self, v):
		self.put(Binary.writeUnsignedVarInt(v))

	def getEntityId(self):
		return self.getVarInt()

	def putEntityId(self, v):
		self.putVarInt(v)

	def getBlockCoords(self, x, y, z):
		x = self.getVarInt()
		y = self.getUnsignedVarInt()
		z = self.getVarInt()

	def putBlockCoords(self, x, y, z):
		self.putVarInt(x)
		self.putUnsignedVarInt(y)
		self.putVarInt(z)

	def getVector3f(self, x, y, z):
		x = self.getLFloat(4)
		y = self.getLFloat(4)
		z = self.getLFloat(4)

	def putVector3f(self, x, y, z):
		self.putLFloat(x)
		self.putLFloat(y)
		self.putLFloat(z)

	def feof(self):
		return isset(self.buffer[self.offset])
