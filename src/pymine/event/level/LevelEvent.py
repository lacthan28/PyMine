# coding=utf-8
from abc import *

from pymine.event.Event import Event
from pymine.level.Level import Level


class LevelEvent(metaclass=ABCMeta, Event):
    level = None

    def __init__(self, level: Level):
        self.level = level

    def getLevel(self):
        return self.level
