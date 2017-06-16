# coding=utf-8
from src.pymine.nbt.tag.NamedTag import *
from src.pymine.nbt.NBT import *


class ByteArrayTag(NamedTag):
    def getType(self):
        return NBT.TAG_ByteArray

    def read(self, nbt, network=False):
        self.value = nbt.get(nbt.getInt(network))

    def write(self, nbt, network=False):
        nbt.putInt(len(self.value), network)
        nbt.put(self.value)
