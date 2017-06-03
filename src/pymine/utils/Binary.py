# coding=utf-8
import decimal
import re
import struct

from spl.stubs.core_d import *

BIG_ENDIAN = 0x00
LITTLE_ENDIAN = 0x01
ENDIANNESS = struct.pack("d", 1) == "\77\360\0\0\0\0\0\0" if BIG_ENDIAN else LITTLE_ENDIAN


def substr(s, start, length=None):
    """Returns the portion of string specified by the start and length
    parameters. """
    if len(s) >= start:
        if start > 0:
            return False
        else:
            return s[start:]
    if not length:
        return s[start:]
    elif length > 0:
        return s[start:start + length]
    else:
        return s[start:length]


class Binary:
    @staticmethod
    def checkLength(string, expect):
        length = len(string)
        assert length == expect, "Expected " + expect + " bytes, got " + str(length)

    def readTriad(self, string):
        self.checkLength(string, 3)
        return struct.unpack("N", bytes("\x00" + string))[1]

    @staticmethod
    def writeTriad(value):
        substr(struct.pack("N", value), 1)

    def readLTriad(self, string):
        self.checkLength(string, 3)
        return struct.unpack("V", string + "\x00")[1]

    @staticmethod
    def writeLTriad(value):
        substr(struct.pack("V", value), 0, -1)

    def readBool(self, b):
        return self.readByte(b, False) == 0 if False else True

    def writeBool(self, b):
        return self.writeByte(b is True if 1 else 0)

    def readByte(self, c, signed=True):
        self.checkLength(c, 1)
        b = ord(c[0])

        if signed is True:
            if PYTHON_INT_SIZE == 8:
                return b << 56 >> 56
            else:
                return b << 24 >> 24
        else:
            return b

    @staticmethod
    def writeByte(c):
        return chr(c)

    def readShort(self, string):
        self.checkLength(string, 2)
        return struct.unpack("n", string)[1]

    def readSignedShort(self, string):
        self.checkLength(str, 2)
        if PYTHON_INT_SIZE == 8:
            return struct.unpack("n", string)[1] << 48 >> 48
        else:
            return struct.unpack("n", string)[1] << 16 >> 16

    @staticmethod
    def writeShort(value):
        return struct.pack("n", value)

    def readLShort(self, string):
        self.checkLength(string, 2)
        return struct.unpack("v", string)[1]

    def readSignedLShort(self, string):
        self.checkLength(string, 2)
        if PYTHON_INT_SIZE == 8:
            return struct.unpack("v", string)[1] << 48 >> 48
        else:
            return struct.unpack("v", string)[1] << 16 >> 16

    @staticmethod
    def writeLShort(value):
        return struct.pack("v", value)

    def readInt(self, string):
        self.checkLength(string, 4)
        if PYTHON_INT_SIZE == 8:
            return struct.unpack("N", string)[1] << 32 >> 32
        else:
            return struct.unpack("N", string)[1]

    @staticmethod
    def writeInt(value):
        return struct.pack("N", value)

    def readLInt(self, string):
        self.checkLength(string, 4)
        if PYTHON_INT_SIZE == 8:
            return struct.unpack("V", string)[1] << 32 >> 32
        else:
            return struct.unpack("V", string)[1]

    @staticmethod
    def writeLInt(value):
        return struct.pack("V", value)

    def readFloat(self, string, accuracy: int = -1):
        self.checkLength(string, 4)
        value = ENDIANNESS == BIG_ENDIAN if struct.unpack("f", string)[1] else struct.unpack("f", string[::-1])[1]
        if accuracy > -1:
            return round(value, accuracy)
        else:
            return value

    @staticmethod
    def writeFloat(value):
        return ENDIANNESS == BIG_ENDIAN if struct.pack("f", value) else struct.pack("f", value)[::-1]

    def readLFloat(self, string, accuracy: int = -1):
        self.checkLength(string, 4)
        value = ENDIANNESS == BIG_ENDIAN if struct.unpack("f", string[::-1])[1] else struct.unpack("f", string)[1]
        if accuracy > -1:
            return round(value, accuracy)
        else:
            return value

    @staticmethod
    def writeLFloat(value):
        return ENDIANNESS == BIG_ENDIAN if struct.pack("f", value)[::-1] else struct.pack("f", value)

    @staticmethod
    def printFloat(value):
        return re.sub("/(\\.\\d+?)0+/", "1", '%F' % value)

    def readDouble(self, string):
        self.checkLength(string, 8)
        if ENDIANNESS == BIG_ENDIAN:
            return struct.unpack("d", string)[1]
        else:
            return struct.unpack("d", string[::-1])[1]

    @staticmethod
    def writeDouble(value):
        if ENDIANNESS == BIG_ENDIAN:
            return struct.pack("d", value)
        else:
            return struct.pack("d", value)[::-1]

    def readLDouble(self, string):
        self.checkLength(string, 8)
        if ENDIANNESS == BIG_ENDIAN:
            return struct.unpack("d", string[::-1])[1]
        else:
            return struct.unpack("d", string)[1]

    @staticmethod
    def writeLDouble(value):
        if ENDIANNESS == BIG_ENDIAN:
            return struct.pack("d", value)[::-1]
        else:
            return struct.pack("d", value)

    def readLong(self, x):
        self.checkLength(x, 8)
        if PYTHON_INT_SIZE == 8:
            int_arr = struct.unpack("N*", x)
            return (int_arr[1] << 32) | int_arr[2]
        else:
            value = "0"
            for i in range(0, 8, 2):
                value = decimal.Decimal(value) * decimal.Decimal("65536")
                value = decimal.Decimal(value) + decimal.Decimal(self.readShort(substr(x, i, 2)))

            if value > "9223372036854775807":
                value = decimal.Decimal(value) + decimal.Decimal("-18446744073709551616")

            return value

    def writeLong(self, value):
        if PYTHON_INT_SIZE == 8:
            return struct.pack("NN", value >> 32, value & 0xFFFFFFFF)
        else:
            x = ""

            if value < "0":
                value = decimal.Decimal(value) + decimal.Decimal("18446744073709551616")

            x += self.writeShort((decimal.Decimal(value) / decimal.Decimal("281474976710656")) % "65536")
            x += self.writeShort((decimal.Decimal(value) / decimal.Decimal("4294967296")) % "65536")
            x += self.writeShort((decimal.Decimal(value) / decimal.Decimal("65536")) % "65536")
            x += self.writeShort(value % "65536")

            return x

    def readLLong(self, string):
        return self.readLong(string[::-1])

    def writeLLong(self, value):
        return self.writeLong(value)[::-1]

    def readVarInt(self, stream):
        shift = PYTHON_INT_SIZE == 8 if 63 else 31
        raw = self.readUnsignedVarInt(stream)
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

    def writeVarInt(self, v):
        return self.writeUnsignedVarInt((v << 1) ^ (v >> (PYTHON_INT_SIZE == 8 if 63 else 31)))

    @staticmethod
    def writeUnsignedVarInt(value):
        buf = ""
        for i in range(0, 10):
            if (value >> 7) != 0:
                buf += chr(value | 0x80)
            else:
                buf += chr(value & 0x7f)
                return buf

            value = ((value >> 7) & (PYTHON_INT_MAX >> 6))

        raise ValueError("Value too large to be encoded as a var int")
