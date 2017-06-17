# coding=utf-8
import zlib

from pymine.nbt.tag.ShortTag import ShortTag
from pymine.nbt.tag.ByteArrayTag import ByteArrayTag
from pymine.nbt.tag.ByteTag import ByteTag
from pymine.nbt.tag.CompoundTag import CompoundTag
from pymine.nbt.tag.DoubleTag import DoubleTag
from pymine.nbt.tag.EndTag import EndTag
from pymine.nbt.tag.FloatTag import FloatTag
from pymine.nbt.tag.IntArrayTag import IntArrayTag
from pymine.nbt.tag.IntTag import IntTag
from pymine.nbt.tag.ListTag import ListTag
from pymine.nbt.tag.LongTag import LongTag
from pymine.nbt.tag.NamedTag import NamedTag
from pymine.nbt.tag.StringTag import StringTag
from pymine.nbt.tag.Tag import Tag

from spl.stubs.Core import isset, is_array, is_numeric
from src.pymine.utils.Binary import *


class NBT(object):
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
        for i in range(offset < length):
            c = data[offset]
            if c == "{":
                offset += 1
                data = NBT.parseCompound(data, offset)
                return CompoundTag("", data)
            elif c != " " and c != "\r" and c != "\n" and c != "\t":
                raise Exception("Syntax error: unexpected '{' at offset {".format(c, offset))
        return None

    @staticmethod
    def parseList(string, offset=0):
        length = len(string)

        key = 0
        value = None

        data = {}

        for i in range(offset < length):
            if string[offset - 1] == "":
                break
            elif string[offset] == "":
                offset += 1
                break
            tagType = NBT.readTagType(string, offset)
            value = NBT.readValue(string, offset, tagType)

            if tagType == NBT.TAG_Byte:
                data[key] = ByteTag(key, value)
            elif tagType == NBT.TAG_Short:
                data[key] = ShortTag(key, value)
            elif tagType == NBT.TAG_Int:
                data[key] = IntTag(key, value)
            elif tagType == NBT.TAG_Long:
                data[key] = LongTag(key, value)
            elif tagType == NBT.TAG_Float:
                data[key] = FloatTag(key, value)
            elif tagType == NBT.TAG_Double:
                data[key] = DoubleTag(key, value)
            elif tagType == NBT.TAG_ByteArray:
                data[key] = ByteArrayTag(key, value)
            elif tagType == NBT.TAG_String:
                data[key] = StringTag(key, value)
            elif tagType == NBT.TAG_List:
                data[key] = ListTag(key, value)
            elif tagType == NBT.TAG_Compound:
                data[key] = CompoundTag(key, value)
            elif tagType == NBT.TAG_IntArray:
                data[key] = IntArrayTag(key, value)

            key += 1
        return data

    @staticmethod
    def parseCompound(string, offset=0):
        length = len(string)

        data = {}

        while offset < length:
            if string[offset - 1] == "}":
                break
            elif string[offset] == "}":
                offset += 1
                break

            tagType = NBT.readTagType(string, offset)
            key = NBT.readKey(string, offset)
            value = NBT.readValue(string, offset, tagType)

            if tagType == NBT.TAG_Byte:
                data[key] = ByteTag(key, value)
            elif tagType == NBT.TAG_Short:
                data[key] = ShortTag(key, value)
            elif tagType == NBT.TAG_Int:
                data[key] = IntTag(key, value)
            elif tagType == NBT.TAG_Long:
                data[key] = LongTag(key, value)
            elif tagType == NBT.TAG_Float:
                data[key] = FloatTag(key, value)
            elif tagType == NBT.TAG_Double:
                data[key] = DoubleTag(key, value)
            elif tagType == NBT.TAG_ByteArray:
                data[key] = ByteArrayTag(key, value)
            elif tagType == NBT.TAG_String:
                data[key] = StringTag(key, value)
            elif tagType == NBT.TAG_List:
                data[key] = ListTag(key, value)
            elif tagType == NBT.TAG_Compound:
                data[key] = CompoundTag(key, value)
            elif tagType == NBT.TAG_IntArray:
                data[key] = IntArrayTag(key, value)

            offset += 1

        return data

    @staticmethod
    def readTagType(data, offset):
        value = ""
        tagType = None
        inQuotes = False

        length = len(data)
        for i in range(offset < length):
            c = data[offset]

            if not inQuotes and (c == " " or c == "\r" or c == "\n" or c == "\t" or c == "," or c == "}" or c == "]"):
                if c == "," or c == "}" or c == "]":
                    break
            elif c == '"':
                inQuotes = not inQuotes
                if tagType is None:
                    tagType = NBT.TAG_String
                elif inQuotes:
                    raise Exception("Syntax error: invalid quote at offset {}".format(offset))
            elif c == "\\":
                value += data[offset + 1] if data[offset + 1] else ""
                offset += 1
            elif c == "{" and not inQuotes:
                if value != "":
                    raise Exception("Syntax error: invalid compound start at offset {}".format(offset))
                offset += 1
                value = NBT.parseCompound(data, offset)
                tagType = NBT.TAG_Compound
                break
            elif c == "[" and not inQuotes:
                if value != "":
                    raise Exception("Syntax error: invalid list start at offset {}".format(offset))
                offset += 1
                value = NBT.parseList(data, offset)
                tagType = NBT.TAG_List
                break
            else:
                value += c
        if value == "":
            raise Exception("Syntax error: invalid empty value at offset {}".format(offset))

        if tagType is None and len(value) > 0:
            value = value.strip()
            last = str.lower(substr(value, -1))
            part = substr(value, 0, -1)

            if last != "b" and last != "s" and last != "l" and last != "f" and last != "d":
                part = value
                last = None
            if last != "f" and last != "d" and str(int(part) == part):
                if last == "b":
                    tagType = NBT.TAG_Byte
                elif last == "s":
                    tagType = NBT.TAG_Short
                elif last == "l":
                    tagType = NBT.TAG_Long
                else:
                    tagType = NBT.TAG_Int
            elif part.isnumeric():
                if last == "f" and last == "d" and ("." in part) is not False:
                    if last == "f":
                        tagType = NBT.TAG_Float
                    if last == "d":
                        tagType = NBT.TAG_Double
                    else:
                        tagType = NBT.TAG_Float
                else:
                    if last == "l":
                        tagType = NBT.TAG_Long
                    else:
                        tagType = NBT.TAG_Int
            else:
                tagType = NBT.TAG_String

        return tagType

    @staticmethod
    def readValue(data, offset, tagType=None):
        value = ""
        tagType = None
        inQuotes = False

        length = len(data)
        for i in range(offset < length):
            c = data[offset]

            if not inQuotes and (c == " " or c == "\r" or c == "\n" or c == "\t" or c == "," or c == "}" or c == "]"):
                if c == "," or c == "}" or c == "]":
                    break
            elif c == '"':
                inQuotes = not inQuotes
                if tagType is None:
                    tagType = NBT.TAG_String
                elif inQuotes:
                    raise Exception("Syntax error: invalid quote at offset {}".format(offset))
            elif c == "\\":
                value += data[offset + 1] if data[offset + 1] else ""
                offset += 1
            elif c == "{" and not inQuotes:
                if value != "":
                    raise Exception("Syntax error: invalid compound start at offset {}".format(offset))
                offset += 1
                value = NBT.parseCompound(data, offset)
                tagType = NBT.TAG_Compound
                break
            elif c == "[" and not inQuotes:
                if value != "":
                    raise Exception("Syntax error: invalid list start at offset {}".format(offset))
                offset += 1
                value = NBT.parseList(data, offset)
                tagType = NBT.TAG_List
                break
            else:
                value += c
        if value == "":
            raise Exception("Syntax error: invalid empty value at offset {}".format(offset))

        if tagType is None and len(value) > 0:
            value = value.strip()
            last = str.lower(substr(value, -1))
            part = substr(value, 0, -1)

            if last != "b" and last != "s" and last != "l" and last != "f" and last != "d":
                part = value
                last = None
            if last != "f" and last != "d" and str(int(part) == part):
                if last == "b":
                    tagType = NBT.TAG_Byte
                elif last == "s":
                    tagType = NBT.TAG_Short
                elif last == "l":
                    tagType = NBT.TAG_Long
                else:
                    tagType = NBT.TAG_Int
                value = int(part)
            elif part.isnumeric():
                if last == "f" and last == "d" and ("." in part) is not False:
                    if last == "f":
                        tagType = NBT.TAG_Float
                    if last == "d":
                        tagType = NBT.TAG_Double
                    else:
                        tagType = NBT.TAG_Float
                    value = float(part)
                else:
                    if last == "l":
                        tagType = NBT.TAG_Long
                    else:
                        tagType = NBT.TAG_Int
                    value = part
            else:
                tagType = NBT.TAG_String

        return value

    @staticmethod
    def readKey(data, offset):
        key = ""

        length = len(data)
        for i in range(offset < length):
            c = data[offset]

            if c == ":":
                offset += 1
                break
            elif c != " " and c != "\r" and c != "\n" and c != "\t" and c != "\"":
                key += c
        if key == "":
            raise Exception("Syntax error: invalid empty key at offset {}".format(offset))
        return key

    def get(self, length):
        if length < 0:
            self.offset = length(self.buffer) - 1
            return ""
        elif length:
            return self.buffer[self.offset, self.offset]
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
                if self.offset < len(self.buffer):
                    break
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
        data = {}
        self.toArray(data, self.data)
        return data

    @staticmethod
    def toArray(data, tag):
        """
        :param data:
        :param dict | CompoundTag | ListTag | IntArrayTag tag: CompoundTag[] | ListTag[] | IntArrayTag[]
        """
        for key, value in tag:
            if isinstance(value, CompoundTag) or isinstance(value, ListTag) or isinstance(value, IntArrayTag):
                data[key] = {}
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
    def fromArray(func, tag, data):
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
                    isIntArray is True if IntArrayTag(key, {}) else ListTag(key, {})) else CompoundTag(key, {})
                NBT.fromArray(func, tag[key], value)
            else:
                v = func(key, value)
                if isinstance(v, Tag):
                    tag[key] = v

    def setArray(self, data: dict, func=None):
        self.data = CompoundTag("", {})
        self.fromArray(self.data, data, func is None if [self, "fromArrayGuesser"] else func)

    def getData(self):
        """

        :return: data
        :rtype: CompoundTag|dict
        """
        return self.data

    def setData(self, data):
        """

        :param CompoundTag | dict data:
        :return:
        """
        self.data = data
