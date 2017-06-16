# coding=utf-8
import zlib
from typing import Callable

from pymine.item.Item import ShortTag
from pymine.nbt.tag.ByteArrayTag import ByteArrayTag
from pymine.nbt.tag.ByteTag import ByteTag
from pymine.nbt.tag.CompoundTag import CompoundTag
from pymine.nbt.tag.DoubleTag import DoubleTag
from pymine.nbt.tag.EndTag import EndTag
from pymine.nbt.tag.ListTag import ListTag
from pymine.nbt.tag.NamedTag import NamedTag
from pymine.nbt.tag.StringTag import StringTag
from pymine.nbt.tag.Tag import Tag
from spl.stubs.Core import isset, is_array, is_numeric
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
    def parseJSON(data, offset=0):
        length = len(data)
        while offset < length:
            c = data[offset]
            if c == "{":
                offset += 1
                data = NBT.parseCompound(data, offset)
                return CompoundTag("", data)
            elif c != " " and c != "\r" and c != "\n" and c != "\t":
                raise Exception("Syntax error: unexpected '{' at offset {".format(c, offset))
            offset += 1
        return None

    @staticmethod  # TODO: chua xong
    def parseList(string, offset=0):
        length = len(string)

        key = 0
        value = None

        data = {

        while offset < length:
            if string[offset - 1] == "":
                break
            elif string[offset] == "":
                offset += 1
                break
            tagType = None
            value = NBT.readValue(string, offset, tagType)

            if tagType == NBT.TAG_Byte:
                data[key] = ByteTag(key, value)

            offset += 1

    @staticmethod  # TODO: chua xong
    def parseCompound(string, offset=0):
        pass

    @staticmethod  # TODO: chua xong
    def readValue(data, offset, tagType=None):
        pass

    @staticmethod  # TODO: chua xong
    def readKey(data, offset):
        pass

    def get(self, length):
        if length < 0:
            self.offset = length(self.buffer) - 1
            return ""
        elif length:
            return self.buffer[self.offset:self.offset]
        self.offset += length
        return length == 1 if self.buffer[self.offset + 1] else self.buffer[(self.offset - length), length]

    def put(self, v):
        self.buffer += v

    def feof(self):
        return not isset(self.buffer[self.offset])

    def __init__(self, endianness=LITTLE_ENDIAN):
        self.offset = 0
        self.endianness = endianness & 0x01

    def read(self, buffer, doMultiple=False, network: bool = False):
        self.offset = 0
        self.buffer = buffer
        self.data = self.readTag(network)
        if doMultiple and self.offset < len(self.buffer):
            self.data = [self.data]
            while True:
                self.data.append(self.readTag(network))
                if self.offset < len(self.buffer): break
            self.buffer = ''

    def readCompressed(self, buffer):
        self.read(zlib.decompress(buffer))

    def readNetworkCompressed(self, buffer):
        self.read(zlib.decompress(buffer), False, True)

    def write(self, network: bool = False):
        self.offset = 0
        self.buffer = ''

        if isinstance(self.data, CompoundTag):
            self.writeTag(self.data, network)
            return self.buffer
        elif is_array(self.data):
            for tag in self.data:
                self.writeTag(tag, network)

            return self.buffer
        return False

    def writeCompressed(self, level=7):
        write = self.write()
        if write is not False:
            return zlib.compress(write, level)
        return False

    def writeNetworkCompressed(self, level=7):
        write = self.write(True)
        if write is not False:
            return zlib.compress(write, level)
        return False

    def readTag(self, network: bool = False):
        if self.feof():
            tagType = -1
        else:
            tagType = self.getByte()

        if tagType == NBT.TAG_Byte:
            tag = ByteTag(self.getString(network))
            tag.read(self, network)
        elif tagType == NBT.TAG_Short:
            tag = ShortTag(self.getString(network))
            tag.read(self, network)
        elif tagType == NBT.TAG_Int:
            tag = IntTag(self.getString(network))
            tag.read(self, network)
        elif tagType == NBT.TAG_Long:
            tag = LongTag(self.getString(network))
            tag.read(self, network)
        elif tagType == NBT.TAG_Float:
            tag = FloatTag(self.getString(network))
            tag.read(self, network)
        elif tagType == NBT.TAG_Double:
            tag = DoubleTag(self.getString(network))
            tag.read(self, network)
        elif tagType == NBT.TAG_ByteArray:
            tag = ByteArrayTag(self.getString(network))
            tag.read(self, network)
        elif tagType == NBT.TAG_String:
            tag = StringTag(self.getString(network))
            tag.read(self, network)
        elif tagType == NBT.TAG_List:
            tag = ListTag(self.getString(network))
            tag.read(self, network)
        elif tagType == NBT.TAG_Compound:
            tag = CompoundTag(self.getString(network))
            tag.read(self, network)
        elif tagType == NBT.TAG_IntArray:
            tag = IntArrayTag(self.getString(network))
            tag.read(self, network)
        else:
            tag = EndTag()

        return tag

    def writeTag(self, tag: Tag, network: bool = False):
        self.putByte(tag.getType())
        if isinstance(tag, NamedTag):
            self.putString(tag.getName(), network)

        tag.write(self, network)

    def getByte(self):
        return Binary.readByte(self.get(1))

    def putByte(self, v):
        self.buffer += Binary.writeByte(v)

    def getShort(self):
        return self.endianness == NBT.BIG_ENDIAN if Binary.readShort(self.get(2)) else Binary.readLShort(self.get(2))

    def putShort(self, v):
        self.buffer += self.endianness == NBT.BIG_ENDIAN if Binary.writeShort(v) else Binary.writeLShort(v)

    def getInt(self, network: bool = False):
        if network is True:
            return Binary.readVarInt(self)
        return self.endianness == NBT.BIG_ENDIAN if Binary.readInt(self.get(4)) else Binary.readLInt(self.get(4))

    def putInt(self, v, network: bool = False):
        if network is True:
            self.buffer += Binary.writeVarInt(v)
        else:
            self.buffer += self.endianness == NBT.BIG_ENDIAN if Binary.writeInt(v) else Binary.writeLInt(v)

    def getLong(self):
        return self.endianness == self.BIG_ENDIAN if Binary.readLong(self.get(8)) else Binary.readLLong(self.get(8))

    def putLong(self, v):
        self.buffer += self.endianness == self.BIG_ENDIAN if Binary.writeLong(v) else Binary.writeLLong(v)

    def getFloat(self):
        return self.endianness == self.BIG_ENDIAN if Binary.readFloat(self.get(4)) else Binary.readLFloat(self.get(4))

    def putFloat(self, v):
        self.buffer += self.endianness == self.BIG_ENDIAN if Binary.writeFloat(v) else Binary.writeLFloat(v)

    def getDouble(self):
        return self.endianness == self.BIG_ENDIAN if Binary.readDouble(self.get(8)) else Binary.readLDouble(self.get(8))

    def putDouble(self, v):
        self.buffer += self.endianness == self.BIG_ENDIAN if Binary.writeDouble(v) else Binary.writeLDouble(v)

    def getString(self, network: bool = False):
        length = None
        if network:
            length = Binary.readUnsignedVarInt(self)
        else:
            length = self.getShort()
        return self.get(length)

    def putString(self, v, network: bool = False):
        if network is True:
            self.put(Binary.writeUnsignedVarInt(len(v)))
        else:
            self.putShort(len(v))

        self.buffer += v

    def getArray(self):
        data = []
        self.toArray(data, self.data)
        return data

    @staticmethod
    def toArray(data: list, tag: list):

        """
        :param list data:
        :param CompoundTag[] | ListTag[] | IntArrayTag[] tag:
        """
        for key, value in tag:
            if isinstance(value, CompoundTag) or isinstance(value, ListTag) or isinstance(value, IntArrayTag):
                data[key] = []
                NBT.toArray(data[key], value)
            else:
                data[key] = value.getValue()

    @staticmethod
    def fromArrayGuesser(key, value):
        if isinstance(value, int):
            return IntTag(key, value)
        elif isinstance(value, float):
            return FloatTag(key, value)
        elif isinstance(value, str):
            return StringTag(key, value)
        elif isinstance(value, bool):
            return ByteTag(key, value if 1 else 0)
        return None

    @staticmethod
    def fromArray(tag: Tag, data=dict, func):
        for key, value in data:
            if is_array(value):
                isNumeric = True
                isIntArray = True
                for k, v in value:
                    if not is_numeric(k):
                        isNumeric = False
                        break
                    elif not isinstance(v, int):
                        isIntArray = False

                tag[key] = isNumeric is True if (
                isIntArray is True if IntArrayTag(key, []) else ListTag(key, [])) else CompoundTag(key, [])
                NBT.fromArray(tag[key], value, guesser)
            else:
                v = guesser(key, value)
                if isinstance(v, Tag):
                    tag[key] = v


def setArray(array data, callable


guesser = null){
    self.data = new
CompoundTag("", [])
self.
    fromArray(self.data, data, guesser == null if [self.


class , "fromArrayGuesser"]:


    guesser

)

/ **
* @ return CompoundTag | array
* /
def getData()


    {


return self.data

/ **
* @ param
CompoundTag | array
data
* /
def setData(data){
    self.data = data
