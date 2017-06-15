# coding=utf-8
import sys
from struct import pack, unpack


class test:


    @staticmethod
    def checkLength(string, expect):
        length = len(string)
        assert length == expect, "Expected " + expect + " bytes, got " + str(length)
    @staticmethod
    def testing(string):
        return string.checkLength(3)

t = test()
print(t.testing("hdsfgsdf"))