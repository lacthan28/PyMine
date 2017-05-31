from ..math.Vector3 import *
from .Level import *


class Position(Vector3):
    level = None

    def __init__(self, x=0, y=0, z=0, level: Level = None):
        self.x = x
        self.y = y
        self.z = z
        self.level = level

    def fromObject(self, pos: Vector3, level: Level = None):
        return Position(pos.x, pos.y, pos.z, level)

    def getLevel(self):
        if self.level is not None and self.level.isClose():
            MainLogger.getLogger().debug("Position was holding a reference to an unloaded Level")
            self.level = None

        return self.level

    def setLevel(self, level: Level = None):
        if level is not None and level.isClose():
            raise ValueError("Specified level has been unloaded and cannot be used")
        self.level = level
        return self

    def isValid(self):
        return isinstance(self.getLevel(), Level)

    def getSide(self, side, step=1):
        assert self.isValid()

        return Position.fromObject(Vector3.getSide(side, step), self.level)

    def __toString(self):
        return "Position(level=" + self.isValid() if self.getLevel().getName() else "null" + ",x=" + self.x + ",y=" + self.y + ",z=" + self.z + ")"

    def setComponents(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        return self