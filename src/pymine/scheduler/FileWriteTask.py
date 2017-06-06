# coding=utf-8
from pymine.scheduler.AsyncTask import AsyncTask


class FileWriteTask(AsyncTask):
    path = None
    contents = None

    def __init__(self, path, contents):
        self.path = path
        self.contents = contents

    def onRun(self):
        try:
            with open(self.path, 'w') as f:
                f.write(self.contents)
        except BaseException as e:
            pass
