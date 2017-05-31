from .Server import *
from .ThreadManager import *
import urllib
from ..spl.ClassLoader import *


class Worker:
    classLoader = None

    isKilled = False

    def check_connectivity(reference):
        try:
            urllib.request.urlopen(reference, timeout=1)
            return True
        except urllib.request.URLError:
            return False

    def getClassLoader(self):
        return self.classLoader

    def setClassLoader(self, loader:ClassLoader=None):
        if loader is None:
            loader = Server.getInstance().getLoader()
        self.classLoader = loader

    def registerClassLoader(self):
        if not has_:
            import src.spl.ClassLoader
            import src.spl.BaseClassLoader

        if self.classLoader is not None:
            self.classLoader.register(True)

    def start(self, options = 0x111111):
        ThreadManager.getInstance().add(self)

        