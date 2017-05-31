import struct, sys, re
import ctypes
import decimal


class Binary:
    BIG_ENDIAN = 0x00
    LITTLE_ENDIAN = 0x01

    def substr(self, s, start, length=None):
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

    def checkLength(self, str, expect):
        assert len(str) == expect, "Expected " + expect + " bytes, got " + len(str)

    def readTriad(self, str):
        self.checkLength(str, 3)
        return struct.unpack("N", "\x00" + str)[1]

    def writeTriad(self, value):
        self.substr(struct.pack("N", value), 1)

    def readLTriad(self, str):
        self.checkLength(str, 3)
        return struct.unpack("V", str + "\x00")[1]

    def writeLTriad(self, value):
        self.substr(struct.pack("V", value), 0, -1)

    def readBool(self, b):
        if self.readByte(b, False) == 0:
            return False
        else:
            return True

    def writeBool(self, b):
        if b == True:
            self.writeByte

    def readByte(self, c, signed=True):
        self.checkLength(c, 1)
        b = ord(c[0])

        if signed is True:
            if ctypes.sizeof(ctypes.c_voidp) == 8:
                return b << 56 >> 56
            else:
                return b << 24 >> 24
        else:
            return b

    def writeByte(c):
        return chr(c)

    def readShort(self, str):
        self.checkLength(str, 2)
        return struct.unpack("n", str)[1]

    def readSignedShort(self, str):
        self.checkLength(str, 2)
        if ctypes.sizeof(ctypes.c_voidp) == 8:
            return struct.unpack("n", str)[1] << 48 >> 48
        else:
            return struct.unpack("n", str)[1] << 16 >> 16

    def writeShort(self, value):
        return struct.pack("n", value)

    def readLShort(self, str):
        self.checkLength(str, 2)
        return struct.unpack("v", str)[1]

    def readSignedLShort(self, str):
        self.checkLength(str, 2)
        if ctypes.sizeof(ctypes.c_voidp) == 8:
            return struct.unpack("v", str)[1] << 48 >> 48
        else:
            return struct.unpack("v", str)[1] << 16 >> 16

    def writeLShort(self, value):
        return struct.pack("v", value)

    def readInt(self, str):
        self.checkLength(str, 4)
        if ctypes.sizeof(ctypes.c_voidp) == 8:
            return struct.unpack("N", str)[1] << 32 >> 32
        else:
            return struct.unpack("N", str)[1]

    def writeInt(self, value):
        return struct.pack("N", value)

    def readLInt(self, str):
        self.checkLength(str, 4)
        if ctypes.sizeof(ctypes.c_voidp) == 8:
            return struct.unpack("V", str)[1] << 32 >> 32
        else:
            return struct.unpack("V", str)[1]

    def writeLInt(self, value):
        return struct.pack("V", value)

    def readFloat(self, str, accuracy=-1):
        self.checkLength(str, 4)
        if sys.byteorder == Binary.BIG_ENDIAN:
            value = struct.unpack("f", str)[1]
        else:
            value = struct.unpack("f", str[::-1])[1]
        if accuracy > -1:
            return round(value, accuracy)
        else:
            return value

    def writeFloat(self, value):
        if sys.byteorder == Binary.BIG_ENDIAN:
            return struct.pack("f", value)
        else:
            return struct.pack("f", value)[::-1]

    def readLFloat(self, str, accuracy=-1):
        self.checkLength(str, 4)
        value = sys.byteorder
        if sys.byteorder == Binary.BIG_ENDIAN:
            value = struct.unpack("f", str[::-1])[1]
        else:
            value = struct.unpack("f", str)[1]
        if accuracy > -1:
            return round(value, accuracy)
        else:
            return value

    def writeLFloat(self, value):
        if sys.byteorder == Binary.BIG_ENDIAN:
            return struct.pack("f", value)[::-1]
        else:
            return struct.pack("f", value)

    def printFloat(self, value):
        return re.sub("/(\\.\\d+?)0+/", "1", '%F' % (value))

    def readDouble(self, str):
        self.checkLength(str, 8)
        if sys.byteorder == Binary.BIG_ENDIAN:
            return struct.unpack("d", str)[1]
        else:
            return struct.unpack("d", str[::-1])[1]

    def writeDouble(self, value):
        if sys.byteorder == Binary.BIG_ENDIAN:
            return struct.pack("d", value)
        else:
            return struct.pack("d", value)[::-1]

    def readLDouble(self, str):
        self.checkLength(str, 8)
        if sys.byteorder == Binary.BIG_ENDIAN:
            return struct.unpack("d", str[::-1])[1]
        else:
            return struct.unpack("d", str)[1]

    def writeLDouble(self, value):
        if sys.byteorder == Binary.BIG_ENDIAN:
            return struct.pack("d", value)[::-1]
        else:
            return struct.pack("d", value)

    def readLong(self, x):
        self.checkLength(x, 8)
        if ctypes.sizeof(ctypes.c_voidp) == 8:
            int = struct.unpack("N*", x)
            return (int[1] << 32) | int[2]
        else:
            value = "0"
            i = 0
            while i < 8:
                decimal.getcontext().prec = 0
                value = decimal.Decimal(value) * decimal.Decimal("65536")
                value = decimal.Decimal(value) + decimal.Decimal(self.readShort(self.substr(x, i, 2)))
                i += 2

            if value > "9223372036854775807":
                value = decimal.Decimal(value) + decimal.Decimal("-18446744073709551616")

            return value

    def writeLong(self, value):
        if ctypes.sizeof(ctypes.c_voidp) == 8:
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

    def readLLong(self, str):
        return self.readLong(str[::-1])

    def writeLLong(self, value):
        return self.writeLong(value)[::-1]

    def readVarInt(self, stream):
        shift = ctypes.sizeof(ctypes.c_voidp) == 8 if 63 else 31
        raw = self.readUnsignedVarInt(stream)
        temp = (((raw << shift) >> shift) ^ raw) >> 1
        return temp ^ (raw & (1 << shift))

    def readUnsignedVarInt(self, stream):
        value = 0
        i = 0
        while b & 0x80:
            if (i > 63):
                raise ValueError("Variant did not terminate after 10 bytes!")
            b = stream.encode("ascii")
            value |= ((b & 0x7f) << i)
            i += 7

        return value

    def writeVarInt(self, v):
        return self.writeUnsignedVarInt((v << 1) ^ (v >> (ctypes.sizeof(ctypes.c_voidp) == 8 if 63 else 31)))

    def writeUnsignedVarInt(self, value):
        buf = ""
        i = 0
        while i < 10:
            if (value >> 7) != 0:
                buf += chr(value | 0x80)
            else:
                buf += chr(value & 0x7f)
                return buf

            value = ((value >> 7) & (sys.maxint >> 6))
            ++i

        raise ValueError("Value too large to be encoded as a varint")
