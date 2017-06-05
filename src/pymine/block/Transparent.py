from .Block import *
from abc import *


class Transparent(metaclass=ABCMeta, Block):
    def isTransparent(self):
        return True
