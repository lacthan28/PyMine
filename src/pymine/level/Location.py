from src.pymine.isset import isset
from .Position import *
from .Level import *
from ..math.Vector3 import *


class Location(Position):
    yaw, pitch = None

    def __init__(self, x=0, y=0, z=0, yaw=0.0, pitch=0.0, level: Level = None):
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.level = level

    def fromObject(self, pos: Vector3, level: Level = None, yaw=0.0, pitch=0.0):
        return Location(pos.x, pos.y, pos.z, yaw, pitch,
                        isset(level) if level else (isinstance(pos, Position) if pos.level else None))

    def getYaw(self):
        return self.yaw

    def getPitch(self):
        return self.pitch

    def __toString(self):
        return "Location (level=" + self.isValid() if self.getLevel().getName() else "null" + ", x=" + self.x + ", y=" + self.y + ", z=" + self.z + ", yaw=" + self.yaw + ", pitch=" + self.pitch + ")"