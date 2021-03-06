# from src.spl.stubs.pthreads import Worker
from .Server import *
from .ThreadManager import *
from ..spl.ClassLoader import *
from rq import Worker, Queue


class Worker(Worker):
    classLoader = None

    isKilled = False

    def __init__(self):
        super(Worker, self).__init__()

    def getClassLoader(self):
        return self.classLoader

    def setClassLoader(self, loader: ClassLoader = None):
        if loader is None:
            loader = Server.getInstance().getLoader()
        self.classLoader = loader

    def registerClassLoader(self):
        if not interface_exists("ClassLoader", False):
            pass

        if self.classLoader is not None:
            self.classLoader.register(True)

    def start(self, options=0x111111):
        ThreadManager.getInstance().add(self)

        if not self.isRunning() and not self.isJoined() and not self.isTerminated():
            if self.getClassLoader() is None:
                self.setClassLoader()

            return Worker.start(options)
        return False
