from array import *

from spl.stubs.isset import *


class TranslationContainer:
    params = []

    def __init__(self, text, params=None):
        self.__init__(text)
        if params is None:
            params = []
        self.setParameters(params)

    def getParameters(self):
        return self.params

    def getParameter(self, i):
        return isset(self.params[i]) if self.params[i] else None

    def setParameter(self, i, string):
        if i < 0 or i > len(self.params):
            raise ValueError("Invalid index " + i + ", have " + str(len(self.params)))

        self.params[int(i)] = string

    def setParameters(self, params: array):
        i = 0
        for s in params:
            self.params[i] = str(s)
            i = ++i
