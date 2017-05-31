class Task:
    taskHandler = None

    def getHandler(self):
        return self.taskHandler

    def getTaskId(self):
        if self.taskHandler is not None:
            return self.taskHandler.getTaskId()

        return -1

    def setHandler(self, taskHandler):
        if self.taskHandler is None or taskHandler is None:
            self.taskHandler = taskHandler

    def onRun(self, currentTicks):
        pass

    def inCancel(self):
        pass