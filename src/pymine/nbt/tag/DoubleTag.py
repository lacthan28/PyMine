# coding=utf-8
from pymine.nbt.NBT import NBT
from pymine.nbt.tag.NamedTag import NamedTag


class DoubleTag(NamedTag):
    def read(self, nbt: NBT, network: bool = False):
        self.value = nbt.getDouble()

    def getType(self):
        return NBT.TAG_Double

    def write(self, nbt: NBT, network: bool = False):
        nbt.putDouble(self.value)
