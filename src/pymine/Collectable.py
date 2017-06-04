from ..spl.stubs.pthreads import *


class Collectable(Threaded, Collectable):
    def __init__(self):
        pass

    varIsGarbage = False

    def isGarbage(self) -> bool:
        return self.varIsGarbage

    def setGarbage(self):
        self.varIsGarbage = True
