import typing

PTHREADS_INHERIT_ALL = 0x111111
PTHREADS_INHERIT_NONE = 0
PTHREADS_INHERIT_INI = 0x1
PTHREADS_INHERIT_CONSTANTS = 0x10
PTHREADS_INHERIT_CLASSES = 0x100
PTHREADS_INHERIT_FUNCTIONS = 0x100
PTHREADS_INHERIT_INCLUDES = 0x10000
PTHREADS_INHERIT_COMMENTS = 0x100000
PTHREADS_ALLOW_HEADERS = 0x1000000
PTHREADS_ALLOW_GLOBALS = 0x10000000


class Collectable:
    def isGarbage(self):
        pass


class iterable:
    pass


class Traversable(iterable):
    pass


class Threaded(Traversable, Collectable):
    def extend(self, obj): pass

    def chunk(self, size, preserve: bool = False): pass

    def count(self): pass

    def isRunning(self): pass

    def isTerminated(self): pass

    def merge(self, _from, overwrite=True): pass

    def notify(self): pass

    def notifyOne(self): pass

    def offsetGet(self, offset): pass

    def offsetSet(self, offset, value): pass

    def offsetExists(self, offset): pass

    def offsetUnset(self, offset): pass

    def pop(self): pass

    def run(self): pass

    def shift(self): pass

    def synchronized(self, function, args=None): pass

    def wait(self, timeout): pass

    def getRefCount(self): pass

    def addRef(self): pass

    def delRef(self): pass

    def isGarbage(self): pass


class Volatile(Threaded):
    pass


class Thread(Threaded):
    def getCreatorId(self): pass

    def getCurrentThread(self): pass

    def getCurrentThreadId(self): pass

    def getThreadId(self): pass

    def isJoined(self): pass

    def isStarted(self): pass

    def join(self): pass

    def start(self, options: int = PTHREADS_INHERIT_ALL): pass


class Worker(Thread):
    def getStacked(self): pass

    def isShutdown(self): pass

    def collector(self, collectable: Collectable): pass

    def shutdown(self): pass

    def stack(self, work: Collectable): pass

    def unstack(self): pass

    def collect(self, function: typing.Callable): pass


class Pool:
    size, _class, workers, ctor, last = None

    def __init__(self, size, _class, ctor=[]): pass

    def collect(self, collector: typing.Callable): pass

    def resize(self, size): pass

    def shutdown(self): pass

    def submit(self, task: Threaded): pass

    def submitTo(self, worker, task: Threaded): pass
