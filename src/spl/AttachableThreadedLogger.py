from .ThreadedLogger import *


class AttachableThreadedLogger(ThreadedLogger):
    attachment = None

    def addAttachment(self, attachment:Th):