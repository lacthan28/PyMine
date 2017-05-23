import BlockIds
from pymine.metadata import Metadatable
from pymine.level import Position

class Block(BlockIds, Metadatable, Position):
    list = None
    fullList = None
    light = None
    