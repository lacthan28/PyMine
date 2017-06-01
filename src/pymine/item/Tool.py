from .Item import *


class Tool(Item):
    TIER_WOODEN = 1
    TIER_GOLD = 2
    TIER_STONE = 3
    TIER_IRON = 4
    TIER_DIAMOND = 5
    TYPE_NONE = 0
    TYPE_SWORD = 1
    TYPE_SHOVEL = 2
    TYPE_PICKAXE = 3
    TYPE_AXE = 4
    TYPE_SHEARS = 5

    def __init__(self, id, meta=0, count=1, name="Unknown"):
        super(Tool, self).__init__()