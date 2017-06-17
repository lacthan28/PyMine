# coding=utf-8
import struct

from pymine.nbt.NBT import NBT
from pymine.nbt.tag.NamedTag import NamedTag


class IntArrayTag(NamedTag):
    def getType(self):
        return NBT.TAG_IntArray

    def write(self, nbt: NBT, network: bool = False):
        nbt.putInt(len(self.value), network)
        if nbt.endianness == NBT.LITTLE_ENDIAN:
            nbt.put(struct.pack("<L" * len(self.value), *self.value))
        else:
            nbt.put(struct.pack(">L" * len(self.value), *self.value))

    def read(self, nbt: NBT, network: bool = False):
        size = nbt.getInt(network)
        if nbt.endianness == NBT.LITTLE_ENDIAN:
            array = struct.unpack("<L" * len(self.value), *nbt.get(size * 4))
        else:
            array = struct.unpack(">L" * len(self.value), *nbt.get(size * 4))
        self.value = [v for key in array for v in key]

    def __str__(self):
        string = type(self).__name__ + "{\n"
        string += ", ".join(self.value)
        return string + "}"
