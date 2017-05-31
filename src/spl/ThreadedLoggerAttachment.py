from .stubs.pthreads import *
from .LoggerAttachment import *


class ThreadedLoggerAttachment(Threaded, LoggerAttachment):
    attachment = None

    def call(self, level, message):
        self.log(level, message)
        if isinstance(self.attachment, ThreadedLoggerAttachment):
            self.attachment.call(level, message)

    def addAttachment(self, ThreadedLoggerAttachment):
        if isinstance(self.attachment, ThreadedLoggerAttachment):
            self.attachment.addAttachment(ThreadedLoggerAttachment.attachment)
        else:
            self.attachment = ThreadedLoggerAttachment.attachment
