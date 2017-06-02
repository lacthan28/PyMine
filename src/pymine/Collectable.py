from ..spl.stubs.pthreads import *


class Collectable(Threaded, Collectable):
    isGarbage = False

    def isGarbage(self) -> bool:
        return self.isGarbage

    def setGarbage(self):
        self.isGarbage = True
