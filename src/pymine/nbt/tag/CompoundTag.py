from typing import List

from .NamedTag import *
from ....spl.stubs.core_c import ArrayAccess
from ..NBT import *


class CompoundTag(NamedTag):
    def __init__(self, name="", value=[]):
        """
        :param name: string
        :param value: NamedTag[]
        """
        super().__init__(name, value)
        self.__name = name
        for tag in value:
            self->[tag.getName()] = tag
