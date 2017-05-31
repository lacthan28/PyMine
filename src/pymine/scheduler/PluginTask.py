from src.pymine.scheduler.Task import *
from src.pymine.plugin.Plugin import *
class PluginTask:

    owner = None

    def __init__(self, owner):
        self.owner = owner

    def getOwner(self):
        return self.owner