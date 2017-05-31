from .Transparent import *


class UnknownBlock(Transparent):
    def isSolid(self):
        return False

    def getHardness(self):
        return 0
