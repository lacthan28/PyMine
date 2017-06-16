# coding=utf-8
import decimal
import re
import struct
import sys

from spl.stubs.Core import substr


def checkLength(string, expect):
	length = len(string)
	assert length == expect, "Expected " + expect + " bytes, got " + str(length)


class Binary:
	BIG_ENDIAN = 'big'
	LITTLE_ENDIAN = 'little'

	@staticmethod
	def readTriad(string):
		checkLength(string, 3)
		return struct.unpack(">L", bytes("\x00" + string))[1]

	@staticmethod
	def writeTriad(value):
		return substr(struct.pack(">L", value), 1)

	@staticmethod
	def readLTriad(string):
		checkLength(string, 3)
		return struct.unpack("<L", string + "\x00")[1]

	@staticmethod
	def writeLTriad(value):
		return substr(struct.pack("<L", value), 0, -1)

	@staticmethod
	def readBool(b):
		return Binary.readByte(b, False) == 0 if False else True

	@staticmethod
	def writeBool(b):
		return Binary.writeByte(b is True if 1 else 0)

	@staticmethod
	def readByte(c, signed = True):
		checkLength(c, 1)
		b = ord(c[0])

		if signed is True:
			if sys.int_info.__getattribute__('sizeof_digit') == 8:
				return b << 56 >> 56
			else:
				return b << 24 >> 24
		else:
			return b

	@staticmethod
	def writeByte(c):
		return chr(c)

	@staticmethod
	def readShort(string):
		checkLength(string, 2)
		return struct.unpack(">h", string.to_bytes())[1]

	@staticmethod
	def readSignedShort(string):
		checkLength(string, 2)
		if sys.int_info.__getattribute__('sizeof_digit') == 8:
			return struct.unpack(">h", string)[1] << 48 >> 48
		else:
			return struct.unpack(">h", string)[1] << 16 >> 16

	@staticmethod
	def writeShort(value):
		return struct.pack(">h", value)

	@staticmethod
	def readLShort(string):
		checkLength(string, 2)
		return struct.unpack("<h", string)[1]

	@staticmethod
	def readSignedLShort(string):
		checkLength(string, 2)
		if sys.int_info.__getattribute__('sizeof_digit') == 8:
			return struct.unpack("<h", string)[1] << 48 >> 48
		else:
			return struct.unpack("<h", string)[1] << 16 >> 16

	@staticmethod
	def writeLShort(value):
		return struct.pack("<h", value)

	@staticmethod
	def readInt(string):
		checkLength(string, 4)
		if sys.int_info.__getattribute__('sizeof_digit') == 8:
			return struct.unpack(">L", string)[1] << 32 >> 32
		else:
			return struct.unpack(">L", string)[1]

	@staticmethod
	def writeInt(value):
		return struct.pack(">L", value)

	@staticmethod
	def readLInt(string):
		checkLength(string, 4)
		if sys.int_info.__getattribute__('sizeof_digit') == 8:
			return struct.unpack("<L", string)[1] << 32 >> 32
		else:
			return struct.unpack("<L", string)[1]

	@staticmethod
	def writeLInt(value):
		return struct.pack("<L", value)

	@staticmethod
	def readFloat(string, accuracy: int = -1):
		checkLength(string, 4)
		value = sys.byteorder == Binary.BIG_ENDIAN if struct.unpack(">f", string)[1] else \
			struct.unpack(">f", string[::-1])[1]
		if accuracy > -1:
			return round(value, accuracy)
		else:
			return value

	@staticmethod
	def writeFloat(value):
		return sys.byteorder == Binary.BIG_ENDIAN if struct.pack(">f", value) else struct.pack(">f", value)[::-1]

	@staticmethod
	def readLFloat(string, accuracy: int = -1):
		checkLength(string, 4)
		value = sys.byteorder == Binary.BIG_ENDIAN if struct.unpack("<f", string[::-1])[1] else \
			struct.unpack("<f", string)[1]
		if accuracy > -1:
			return round(value, accuracy)
		else:
			return value

	@staticmethod
	def writeLFloat(value):
		return sys.byteorder == Binary.BIG_ENDIAN if struct.pack("<f", value)[::-1] else struct.pack("<f", value)

	@staticmethod
	def printFloat(value):
		return re.sub("/(\\.\\d+?)0+$/", "1", '%F' % value)

	@staticmethod
	def readDouble(string):
		checkLength(string, 8)
		if sys.byteorder == Binary.BIG_ENDIAN:
			return struct.unpack(">d", string)[1]
		else:
			return struct.unpack(">d", string[::-1])[1]

	@staticmethod
	def writeDouble(value):
		if sys.byteorder == Binary.BIG_ENDIAN:
			return struct.pack(">d", value)
		else:
			return struct.pack(">d", value)[::-1]

	@staticmethod
	def readLDouble(string):
		checkLength(string, 8)
		if sys.byteorder == Binary.BIG_ENDIAN:
			return struct.unpack("<d", string[::-1])[1]
		else:
			return struct.unpack("<d", string)[1]

	@staticmethod
	def writeLDouble(value):
		if sys.byteorder == Binary.BIG_ENDIAN:
			return struct.pack("<d", value)[::-1]
		else:
			return struct.pack("<d", value)

	@staticmethod
	def readLong(x):
		checkLength(x, 8)
		if sys.int_info.__getattribute__('sizeof_digit') == 8:
			int_arr = struct.unpack(">L*", x)
			return (int_arr[1] << 32) | int_arr[2]
		else:
			value = "0"
			for i in range(0, 8, 2):
				value = decimal.Decimal(value) * decimal.Decimal("65536")
				value = decimal.Decimal(value) + decimal.Decimal(Binary.readShort(substr(x, i, 2)))

			if value > "9223372036854775807":
				value = decimal.Decimal(value) + decimal.Decimal("-18446744073709551616")

			return value

	@staticmethod
	def writeLong(value):
		if sys.int_info.__getattribute__('sizeof_digit') == 8:
			return struct.pack(">LL", value >> 32, value & 0xFFFFFFFF)
		else:
			x = ""

			if value < "0":
				value = decimal.Decimal(value) + decimal.Decimal("18446744073709551616")

			x += Binary.writeShort((decimal.Decimal(value) / decimal.Decimal("281474976710656")) % "65536")
			x += Binary.writeShort((decimal.Decimal(value) / decimal.Decimal("4294967296")) % "65536")
			x += Binary.writeShort((decimal.Decimal(value) / decimal.Decimal("65536")) % "65536")
			x += Binary.writeShort(value % "65536")

			return x

	@staticmethod
	def readLLong(string):
		return Binary.readLong(string[::-1])

	@staticmethod
	def writeLLong(value):
		return Binary.writeLong(value)[::-1]

	@staticmethod
	def readVarInt(stream):
		shift = sys.int_info.__getattribute__('sizeof_digit') == 8 if 63 else 31
		raw = Binary.readUnsignedVarInt(stream)
		temp = (((raw << shift) >> shift) ^ raw) >> 1
		return temp ^ (raw & (1 << shift))

	@staticmethod
	def readUnsignedVarInt(stream):
		value = 0
		b = stream.encode("ascii")
		for i in range(stream.encode("ascii"), b & 0x80, 7):
			if i > 63:
				raise ValueError("Var int did not terminate after 10 bytes!")
			value |= ((b & 0x7f) << i)

		return value

	@staticmethod
	def writeVarInt(v):
		return Binary.writeUnsignedVarInt(
				(v << 1) ^ (v >> (sys.int_info.__getattribute__('sizeof_digit') == 8 if 63 else 31)))

	@staticmethod
	def writeUnsignedVarInt(value):
		buf = ""
		for i in range(0, 10):
			if (value >> 7) != 0:
				buf += chr(value | 0x80)
			else:
				buf += chr(value & 0x7f)
				return buf

			value = ((value >> 7) & (sys.maxsize >> 6))

		raise ValueError("Value too large to be encoded as a var int")
