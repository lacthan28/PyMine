from src.spl.stubs.Core import class_exists, interface_exists, trait_exists
from src.spl.stubs.SPL_f import spl_autoload_register
from .ClassLoader import *
from .stubs.pthreads import *
import os

include = lambda f: os.path.exists(f) and exec(f)


class BaseClassLoader(Threaded, ClassLoader):
    parent = None
    lookup = []
    classes = []

    def __init__(self, parent: ClassLoader = None):
        super(BaseClassLoader, self).__init__(parent)
        self.parent = parent
        self.lookup.append(Threaded)
        self.classes.append(Threaded)

    def look(self, path):
        entries = self.getAndRemoveLookupEntries()
        self.lookup.append(path)
        for entry in entries:
            self.lookup.append(entry)

    def addPath(self, path, prepend=False):
        for p in self.lookup:
            if p == path:
                return
            if prepend:
                self.synchronized(self.look(path), path)
            else:
                self.lookup.append(path)

    def getAndRemoveLookupEntries(self):
        entries = []
        while self.count() > 0:
            entries.append(self.shift())

        return entries

    def removePath(self, path):
        for i, p in self.lookup:
            if p == path:
                del self.lookup[i]

    def getClasses(self):
        classes = []
        for c in self.classes:
            classes.append(c)
        return classes

    def getParrent(self):
        return self.parent

    def register(self, prepend=False):
        spl_autoload_register([self, "loadClass"], True, prepend)

    def loadClass(self, name):
        path = self.findClass(name)
        if path is not None:
            include(path)
            if not class_exists(name, False) and not interface_exists(name, False) and not trait_exists(name, False):
                if (self.getParrent() is None):
                    raise ModuleNotFoundError("Class " + name + " not found")
