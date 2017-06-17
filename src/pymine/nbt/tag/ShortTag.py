# coding=utf-8
from pymine.nbt.NBT import NBT
from pymine.nbt.tag.NamedTag import NamedTag


class ShortTag(NamedTag):
    def getType(self):
        return NBT.TAG_Short

    def write(self, nbt: NBT, network: bool = False):
        nbt.putShort(self.value)

    def read(self, nbt: NBT, network: bool = False):
        self.value = nbt.getShort()
