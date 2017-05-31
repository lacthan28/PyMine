from src.pymine.event.TextContainer import *


class TranslationContainer:
    params = []

    def __init__(self, text, params=[]):
        self.__init__(text)
        self.setParameters(params)

    def getParameters(self):
        return self.params

    def isset(variable):
        return variable in locals() or variable in globals()

    def getParameter(self, i):
        return self.isset(self.params[i]) if self.params[i] else None

    def setParameter(self, i, str):
        if i < 0 or i > len(self.params):
            raise ValueError("Invalid index " + i + ", have " + len(self.params))

        self.params[int(i)] = str

    def setParameters(self, params):
        i = 0
        for s in params:
            self.params[i] = str(s)
            ++i