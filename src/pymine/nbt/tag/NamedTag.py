# coding=utf-8
from .Tag import *


class NamedTag(Tag):
    __name = None

    def __init__(self, name="", value=None):
        """
        :type name: string
        :type value: bool|float|double|int|ByteTag|ShortTag|array|CompoundTag|ListTag|string
        """
        self.__name = (name is None or name is False) if "" else name
        if value is not None:
            self.value = value

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name
