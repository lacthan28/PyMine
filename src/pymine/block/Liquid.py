from .Transparent import *


class Liquid(Transparent):
    temporalVector = None

    def hasEntityCollision(self):
        return True

    def isBreakable(self, item: Item):
        return False

    def canBeReplaced(self):
        return True

    def isSolid(self):
        return False

    adjacentSources = 0
    isOptimalFlowDirection = [0, 0, 0, 0]
    flowCost = [0, 0, 0, 0]

    def getFluidHeightPercent(self):
        d = self.meta
        if d >= 8:
            d = 0

        return (d + 1) / 9

    def getFlowDecay(self, pos: Vector3):
        if not isinstance(pos, Block):
            pos = self.getLevel().getBlock(pos)

        if pos.getId() is not self.getId():
            return -1
        else:
            return pos.getDamage()

    def getEffectiveFlowDecay(self, pos: Vector3):
        if not isinstance(pos, Block):
            pos = self.getLevel().getBlock(pos)

        if pos.getId() is not self.getId():
            return -1

        decay = pos.getDamage()

        if decay >= 8:
            decay = 0

        return decay

    def getFlowVector(self):
        vector = Vector3(0, 0, 0)

        if self.temporalVector is None:
            self.temporalVector = Vector3(0, 0, 0)

        decay = self.getEffectiveFlowDecay(self)

        for j in range(4):
            x = self.x
            y = self.y
            z = self.z

            if j == 0:
                x -= 1
            elif j == 1:
                x += 1
            elif j == 2:
                z -= 1
            elif j == 3:
                z += 1

            sideBlock = self.getLevel().getBlock(self.temporalVector.setComponents(x, y, z))
            blockDecay = self.getEffectiveFlowDecay(sideBlock)

            if blockDecay < 0:
                if not sideBlock.canBeFlowedInto():
                    continue

                blockDecay = self.getEffectiveFlowDecay(
                    self.getLevel().getBlock(self.temporalVector.setComponents(x, y - 1, z)))

                if blockDecay>=0:
                    realDecay = blockDecay - (decay - 8)
                    vector.x += (sideBlock.x - self.x) * realDecay
                    vector.y += (sideBlock.y - self.y) * realDecay
                    vector.z += (sideBlock.z - self.z) * realDecay

                continue
            else:
                realDecay = blockDecay - decay
                vector.x += (sideBlock.x - self.x) * realDecay
                vector.y += (sideBlock.y - self.y) * realDecay
                vector.z += (sideBlock.z - self.z) * realDecay

        if self.getDamage() >= 8:
            falling = False

