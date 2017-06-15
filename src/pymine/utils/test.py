# coding=utf-8
import sys
from struct import pack, unpack


def checkLength(string, expect):
    length = len(string)
    assert length == expect, "Expected " + expect + " bytes, got " + str(length)


def readByte(c, signed=True):
    checkLength(c, 1)
    b = ord(c[0])

    if signed is True:
        if sys.int_info.__getattribute__('sizeof_digit') == 8:
            return b << 56 >> 56
        else:
            return b << 24 >> 24
    else:
        return b


def writeByte(c):
    return chr(c)


s = readByte('A')
print(s)
print(writeByte(s))
