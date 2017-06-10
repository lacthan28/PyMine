# coding=utf-8
from src.pymine.utils.Binary import *


class NBT:
    LITTLE_ENDIAN = 0
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

    def __init__(self, endianness=LITTLE_ENDIAN):
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

    def getInt(self, network=False):
        if network is True:
            return Binary.readVarInt(self)
        return self.endianness == NBT.BIG_ENDIAN if Binary.readInt(self.get(4)) else Binary.readLInt(self.get(4))
