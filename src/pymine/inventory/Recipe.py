# coding=utf-8
from ..utils.UUID import *


class Recipe:
    """
    @:return: pymine.item.Item
    """

    def getResult(self): pass

    def registerToCraftingManager(self): pass

    """
    @:return: UUID
    """

    def getId(self): pass

    def setId(self, id: UUID): pass
