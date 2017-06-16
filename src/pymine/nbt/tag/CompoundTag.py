# -*- coding: utf-8 -*-
from pymine.nbt.tag.EndTag import EndTag
from spl.stubs.Core import ArrayAccess
from .NamedTag import *

from ..NBT import *


class CompoundTag(NamedTag, ArrayAccess):
    def __init__(self, name="", value=None):
        """
        :param str name:
        :param dict value: NamedTag[]
        """
        super().__init__(name, value)
        if value is None:
            value = {}
        self.__name = name
        for tag in value:
            self[tag.getName()] = tag

    def getCount(self):
        count = 0
        for tag in self:
            if isinstance(tag, Tag):
                count += 1

        return count

    def keyExists(self, offset):
        return isset(self[offset]) and isinstance(self[offset], Tag)

    def __getitem__(self, offset):
        if isset(self[offset]) and isinstance(self[offset], Tag):
            if isinstance(self[offset], ArrayAccess):
                return self[offset]
            else:
                return self[offset].getValue()
        assert False, "Offset {} not found".format(offset)

    def __setitem__(self, offset, value):
        if isinstance(value, Tag):
            self[offset] = value
        elif isset(self[offset]) and isinstance(self[offset], Tag):
            self[offset].setValue(value)

    def __delitem__(self, offset):
        del self[offset]

    def getType(self):
        return NBT.TAG_Compound

    def read(self, nbt: NBT, network: bool = False):
        self.value = {}
        while True:
            tag = nbt.readTag(network)
            if isinstance(tag, NamedTag) and tag.getName() != "":
                self[tag.getName()] = tag
            if not isinstance(tag, EndTag) and not nbt.feof():
                break

    def write(self, nbt: NBT, network: bool = False):
        for tag in self:
            if isinstance(tag, Tag) and not isinstance(tag, EndTag):
                nbt.writeTag(tag, network)
        nbt.writeTag(EndTag(), network)

    def __str__(self):
        string = type(self).__name__ + "{\n"
        for tag in self:
            if isinstance(tag, Tag):
                string += type(tag).__name__ + ":" + tag.__str__() + "\n"

        return string + "}"
