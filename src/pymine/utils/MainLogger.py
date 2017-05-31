from .TextFormat import *
from ...spl.LogLevel import *
from ..Thread import *
from ..Worker import *
from ...spl.AttachableThreadedLogger import *
from ...spl.stubs.core_c import *
from ...spl.stubs.core_d import *
from os import *
from re import *

logger = None

def isset(variable):
	return variable in locals() or variable in globals()

class MainLogger(AttachableThreadedLogger):
    logFile, logStream, shutdown, logDebug, logResource = None

    def __init__(self, logFile, logDebug=False):
        global logger
        if isinstance(logger, MainLogger):
            raise RuntimeError("MainLogger has been already created")

        logger = self
        utime(self.logFile)
        self.logFile = logFile
        self.logDebug = logDebug
        self.logStream = Threaded()
        self.start()

    def getLogger(self):
        return logger

    def emergency(self, message):
        self.send(message, LogLevel.EMERGENCY, "EMERGENCY", TextFormat.RED)

    def alert(self, message):
        self.send(message, LogLevel.ALERT, "ALERT", TextFormat.RED)

    def critical(self, message):
        self.send(message, LogLevel.CRITICAL, "CRITICAL", TextFormat.RED)

    def error(self, message):
        self.send(message, LogLevel.ERROR, "ERROR", TextFormat.DARK_RED)

    def warning(self, message):
        self.send(message, LogLevel.WARNING, "WARNING", TextFormat.YELLOW)

    def notice(self, message):
        self.send(message, LogLevel.NOTICE, "NOTICE", TextFormat.AQUA)

    def info(self, message):
        self.send(message, LogLevel.INFO, "INFO", TextFormat.WHITE)

    def debug(self, message):
        if self.logDebug == False:
            return
        self.send(message, LogLevel.DEBUG, "DEBUG", TextFormat.GRAY)

    def setLogDebug(self, logDebug):
        self.logDebug = bool(logDebug)

    def logException(self, e: Throwable, trace=None):
        if trace == None:
            trace = e.getTrace()

        errstr = e.getMessage()
        errfile =e.getFile()
        errno = e.getCode()
        errline = e.getLine()

        errorConversion = {0: "EXCEPTION",
                           E_ERROR: "E_ERROR",
                           E_WARNING: "E_WARNING",
                           E_PARSE: "E_PARSE",
                           E_NOTICE: "E_NOTICE",
                           E_CORE_ERROR: "E_CORE_ERROR",
                           E_CORE_WARNING: "E_CORE_WARNING",
                           E_COMPILE_ERROR: "E_COMPILE_ERROR",
                           E_COMPILE_WARNING: "E_COMPILE_WARNING",
                           E_USER_ERROR: "E_USER_ERROR",
                           E_USER_WARNING: "E_USER_WARNING",
                           E_USER_NOTICE: "E_USER_NOTICE",
                           E_STRICT: "E_STRICT",
                           E_RECOVERABLE_ERROR: "E_RECOVERABLE_ERROR",
                           E_DEPRECATED: "E_DEPRECATED",
                           E_USER_DEPRECATED: "E_USER_DEPRECATED",
                           };
        if errno == 0:
            type = LogLevel.CRITICAL
        else:
            type = (errno == E_ERROR or errno == E_USER_ERROR) if LogLevel.ERROR else ((errno == E_USER_WARNING or errno == E_WARNING) if LogLevel.WARNING else LogLevel.NOTICE)
        errno = isset(errorConversion[errno]) if errorConversion[errno] else errno
        errstr = sub('/\s+/', ' ', str(errstr).trip())
        errfile= pymine\cleanPath(errfile)


        def send(self, message, level, param, color):
            pass
