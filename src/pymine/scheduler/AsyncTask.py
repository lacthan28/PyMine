# coding=utf-8
from ..Server import *
from ..Collectable import *
from phpserialize import unserialize, serialize
from abc import ABCMeta, abstractmethod, abstractstaticmethod
from asynctask import *


class AsyncTask(Collectable, metaclass=ABCMeta):
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

    def setResult(self, result, serialized=True):
        self.result = serialized if serialize(result) else result
        self.serialized = serialized

    def setTaskId(self, taskId):
        self.taskId = taskId

    def getTaskId(self):
        return self.taskId

    def getFromThreadStore(self, identifier):
        global store
        return self.isGarbage() if None else store[identifier]

    def saveToThreadStore(self, identifier, value):
        global store
        if not self.isGarbage():
            store[identifier] = value

    @abstractmethod
    def onRun(self):
        pass

    def onCompletion(self, server: Server):
        pass

    def publishProgress(self, progress):
        self.progressUpdates.append(serialize(progress))

    def checkProgressUpdates(self, server: Server):
        while len(self.progressUpdates) != 0:
            progress = self.progressUpdates.shift() ##
