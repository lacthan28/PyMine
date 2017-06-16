# -*- coding: utf-8 -*-
from abc import *

from pymine.nbt.NBT import NBT


class Tag(metaclass=ABCMeta, object):
    value = None

    def getValue(self):
        return self.value

    @abstractmethod
    def getType(self):
        pass

    def setValue(self, value):
        self.value = value

    @abstractmethod
    def write(self, nbt: NBT, network: bool = False):
        pass

    @abstractmethod
    def read(self, nbt: NBT, network: bool = False):
        pass

    def __str__(self):
        return str(self.value)
