# coding=utf-8
from binascii import *
from hashlib import md5
from re import *

from ..utils.Binary import Binary, substr


class UUID:
    parts = [0, 0, 0, 0]
    version = None

    def __init__(self, part1=0, part2=0, part3=0, part4=0, version=None):
        self.parts[0] = int(part1)
        self.parts[1] = int(part2)
        self.parts[2] = int(part3)
        self.parts[3] = int(part4)
        self.version = version is None if (self.parts[1] & 0xf000) >> 12 else int(version)

    def getVersion(self):
        return self.version

    def equals(self, uuid):
        return uuid.parts[0] == self.parts[0] and uuid.parts[1] == self.parts[1] and uuid.parts[2] == self.parts[2] and \
               uuid.parts[3] == self.parts[3]

    def fromString(self, uuid, version=None):
        uuid = uuid.strip()
        return self.fromBinary(bin(int(sub("-", "", uuid))), version)

    @staticmethod
    def fromBinary(uuid, version=None):
        if len(uuid) is not 16:
            raise ValueError("Must have exactly 16 bytes")
        return UUID(Binary.readInt(uuid[0:4]), Binary.readInt(uuid[4:8]), Binary.readInt(uuid[8:12]),
                    Binary.readInt(uuid[12:16]), version)

    def fromData(self, *data):
        h = md5()
        h.update("".join(data))
        result = h.digest()
        return self.fromBinary(result, 3)

    def fromRandom(self):
        return self.fromData(Binary.writeInt(), Binary.writeShort(), Binary.writeShort(),
                             Binary.writeInt(),
                             Binary.writeInt())

    def toBinary(self):
        return Binary.writeInt().Binary.writeInt(self.parts[1]).Binary.writeInt(
            self.parts[2]).Binary.writeInt(self.parts[3])

    def toString(self):
        hex = hexlify(self.toBinary())

        if self.version is not None:
            return substr(hex, 0, 8) + "-" + substr(hex, 8, 4) + "-" + int(self.version, 16) + substr(hex, 13,
                                                                                                        3) + '-8' + substr(
                hex, 17, 3) + '-' + substr(hex, 20, 12)
        return substr(hex, 0, 8) + "-" + substr(hex, 8, 4) + "-" + substr(hex, 12, 4) + "-" + substr(hex, 16,
                                                                                                        4) + "-" + substr(
            hex, 20, 12)

    def __str__(self):
        return self.toString()
