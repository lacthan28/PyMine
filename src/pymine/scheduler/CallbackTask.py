from src.pymine.scheduler.Task import *
class CallbackTask(Task):
    callable = None
    args = None

    def __init__(self, callable, args=[]):
        self.callable = callable
        self.args = args
        self.args = self

    def getCallable(self):
        return self.callable

    def onRun(self, currentTicks):
        eval(self.callable)(self.args)
