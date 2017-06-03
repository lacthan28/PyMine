# coding=utf-8
from ..Server import *
from ..Collectable import *
from phpserialize import unserialize


class AsyncTask(Collectable):
    worker = None

    progressUpdates = None

    result = None
    serialized = False
    varCancelRun = False

    taskId = None
    crashed = False

    def __init__(self, complexData=None):
        if complexData is None:
            return

        Server.getInstance().getScheduler().storeLocalComplex(self, complexData)

    def run(self):
        self.result = None

        if self.cancelRun is not True:
            try:
                self.onRun()
            except BaseException as e:
                self.crashed = True
                self.worker.handleException(e)

        self.setGarbage()

    def isCrashed(self):
        return self.crashed

    def getResult(self):
        return self.serialized if unserialize(self.result) else self.result

    def cancelRun(self):
        self.varCancelRun = True

    def hasCancelledRun(self):
        return self.varCancelRun == True

    def hasResult(self):
        return self.result is not None

    def setResult(self, result):
