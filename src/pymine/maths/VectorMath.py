from src.pymine.maths.Vector2 import *
class VectorMath:
    def getDirection2D(self, azimuth):
        return Vector2(math.cos(azimuth), math.sin(azimuth))