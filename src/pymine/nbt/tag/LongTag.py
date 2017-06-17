# coding=utf-8
from pymine.nbt.NBT import NBT
from pymine.nbt.tag.NamedTag import NamedTag


class LongTag(NamedTag):
    def getType(self):
        return NBT.TAG_Long

    # TODO: check if this also changed to varint

    def write(self, nbt: NBT, network: bool = False):
        nbt.putLong(self.value)

    def read(self, nbt: NBT, network: bool = False):
        self.value = nbt.getLong()
