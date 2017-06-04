from threading import Thread
from src.pymine.Server import *


class Thread(Thread):
    def __init__(self):
        pass

    classLoader = None
    isKilled = False

    def getClassLoader(self):
        return self.classLoader

    def setClassLoader(self, loader=None):
        if loader is None:
            loader = Server.getInstance().getLoader()
        self.classLoader = loader

    def registerClassLoader(self):
        pass
