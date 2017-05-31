from .Logger import *
from .stubs.pthreads import *
class ThreadedLogger(Logger, Thread):
    pass