from math import *
from .Vector2 import *


class Vector3(object):
    SIDE_DOWN = 0
    SIDE_UP = 1
    SIDE_NORTH = 2
    SIDE_SOUTH = 3
    SIDE_WEST = 4
    SIDE_EAST = 5

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def getFloorX(self):
        return math.floor(self.x)

    def getFloorY(self):
        return math.floor(self.y)

    def getFloorZ(self):
        return math.floor(self.z)

    def getRight(self):
        return self.x

    def getUp(self):
        return self.y

    def getForward(self):
        return self.z

    def getSouth(self):
        return self.x

    def getWest(self):
        return self.z

    """
    :param Vector3
    :param x: int
    :param y: int
    :param z: int
    :return: Vector3
    """

    def add(self, x, y=0, z=0):
        if isinstance(x, Vector3):
            return Vector3(self.x + x.x, self.y + x.y, self.z + x.z)
        else:
            return Vector3(self.x + x, self.y + y, self.z + z)

    """
    :param Vector3
    :param x: int
    :param y: int
    :param z: int
    :return: Vector3
    """

    def substract(self, x=0, y=0, z=0):
        if isinstance(x, Vector3):
            return self.add(-x.x, -x.y, -x.z)
        else:
            return self.add(-x, -y, -z)

    def multiply(self, number):
        return Vector3(self.x * number, self.y * number, self.z * number)

    def divide(self, number):
        return Vector3(int(self.x / number), int(self.y / number), int(self.z / number))

    def ceil(self):
        return Vector3(int(math.ceil(self.x)), int(math.ceil(self.y)), int(math.ceil(self.z)))

    def floor(self):
        return Vector3(int(math.floor(self.x)), int(math.floor(self.y)), int(math.floor(self.z)))

    def round(self):
        return Vector3(int(round(self.x)), int(round(self.y)), int(round(self.z)))

    def abs(self):
        return Vector3(int(math.fabs(self.x)), int(math.fabs(self.y)), int(math.fabs(self.z)))

    def getSide(self, side, step=1):
        if side == Vector3.SIDE_DOWN:
            return Vector3(self.x, self.y - step, self.z)
        elif side == Vector3.SIDE_UP:
            return Vector3(self.x, self.y + step, self.z)
        elif side == Vector3.SIDE_NORTH:
            return Vector3(self.x, self.y, self.z - step)
        elif side == Vector3.SIDE_SOUTH:
            return Vector3(self.x, self.y, self.z + step)
        elif side == Vector3.SIDE_WEST:
            return Vector3(self.x - step, self.y, self.z)
        elif side == Vector3.SIDE_EAST:
            return Vector3(self.x + step, self.y, self.z)
        else:
            return self

    """
    Returns the Vector3 side number opposite the specified one
    :param side: (int) 0-5 one of the SIDE_* constants
    :return: int
    :throws: \InvalidArgumentException if an invalid side is supplied
    """

    def getOppositeSide(self, side: int):
        if side >= 0 and side <= 5:
            return int(side ^ 0x01)
        raise ValueError("Invalid side " + str(side) + " given to getOppositeSide")

    def distanceSquared(self, other):
        return math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2) + math.pow(self.z - other.z, 2)

    def distance(self, other):
        return math.sqrt(self.distanceSquared(other))

    def maxPlainDistance(self, x=0, z=0):
        if isinstance(x, Vector3):
            return self.maxPlainDistance(x.x, x.z)
        elif isinstance(x, Vector2):
            return self.maxPlainDistance(x.x, x.y)
        else:
            return max(math.fabs(self.x - x), math.fabs(self.z - z))

    def lengthsquared(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def length(self):
        return math.sqrt(self.lengthsquared())

    def normalize(self):
        len = self.lengthsquared()
        if len > 0:
            return self.divide(math.sqrt(len))
        return Vector2(0, 0, 0)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def equals(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    """
    Returns a new vector with x value equal to the second parameter, along the line between this vector
    and the passed in vector, or null if not possible.
    :param other: Vector3
    :param num: float
    :return: Vector3
    """

    def getIntermediateWithXValue(self, other, num):
        xDiff = other.x - self.x
        yDiff = other.y - self.y
        zDiff = other.z - self.z

        if (xDiff * xDiff) < 0.0000001:
            return None

        f = (num - self.x) / xDiff

        if f < 0 or f > 1:
            return None
        else:
            return Vector3(self.x + xDiff * f, self.y + yDiff * f, self.z + zDiff * f)

    """
    Returns a new vector with y value equal to the second parameter, along the line between this vector
    and the passed in vector, or null if not possible.
    :param other: Vector3
    :param num: float
    :return: Vector3
    """

    def getIntermediateWithYValue(self, other, num):
        xDiff = other.x - self.x
        yDiff = other.y - self.y
        zDiff = other.z - self.z

        if (yDiff * yDiff) < 0.0000001:
            return None

        f = (num - self.y) / yDiff

        if f < 0 or f > 1:
            return None
        else:
            return Vector3(self.x + xDiff * f, self.y + yDiff * f, self.z + zDiff * f)

    """
    Returns a new vector with z value equal to the second parameter, along the line between this vector
    and the passed in vector, or null if not possible.
    :param other: Vector3
    :param num: float
    :return: Vector3
    """

    def getIntermediateWithZValue(self, other, num):
        xDiff = other.x - self.x
        yDiff = other.y - self.y
        zDiff = other.z - self.z

        if (zDiff * zDiff) < 0.0000001:
            return None

        f = (num - self.z) / zDiff

        if f < 0 or f > 1:
            return None
        else:
            return Vector3(self.x + xDiff * f, self.y + yDiff * f, self.z + zDiff * f)

        """
        :param x:
        :param y:
        :param z:
        :return: Vector3
        """

        def setComponents(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z
            return self

        def __toString(self):
            return "Vector3(x=" + self.x + ", y=" + self.y + ", z=" + self.z + ")"
