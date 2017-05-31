from .Logger import *


class AttachableLogger(Logger):
    def addAttachment(self, LoggerAttachment): pass

    def removeAttachment(self, LoggerAttachment): pass

    def removeAttachments(self): pass

    def getAttachments(self): pass
