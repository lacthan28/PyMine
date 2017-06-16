# coding=utf-8
from pymine.nbt.NBT import NBT
from pymine.nbt.tag.NamedTag import NamedTag


class IntTag(NamedTag):
    def read(self, nbt: NBT, network: bool = False):
        self.value = nbt.getInt(network)

    def getType(self):
        return NBT.TAG_Int

    def write(self, nbt: NBT, network: bool = False):
        nbt.putInt(self.value, network)
