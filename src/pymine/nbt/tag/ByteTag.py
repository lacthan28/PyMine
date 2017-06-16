# -*- coding: utf-8 -*-
from pymine.nbt.NBT import NBT
from pymine.nbt.tag.NamedTag import NamedTag


class ByteTag(NamedTag):
    def getType(self):
        return NBT.TAG_Byte

    def write(self, nbt: NBT, network: bool = False):
        nbt.putByte(self.value)

    def read(self, nbt: NBT, network: bool = False):
        self.value = nbt.getByte()
