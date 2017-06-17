# coding=utf-8
from pymine.nbt.NBT import NBT
from pymine.nbt.tag.NamedTag import NamedTag


class FloatTag(NamedTag):
    def getType(self):
        return NBT.TAG_Float

    def write(self, nbt: NBT, network: bool = False):
        nbt.putFloat(self.value)

    def read(self, nbt: NBT, network: bool = False):
        self.value = nbt.getFloat()
