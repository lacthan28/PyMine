# -*- coding: utf-8 -*-
import linecache
import logging

from .TextFormat import *
from ...spl.LogLevel import *
from ..Thread import *
from ..Worker import *
from ...spl.AttachableThreadedLogger import *
from os import *
from re import *
from threading import Thread, current_thread
import traceback
from pymine.PyMine import *


class MainLogger(AttachableThreadedLogger):
	logFile = None
	logStream = None
	isShutdown = None
	logDebug = None
	logResource = None

	logger = None

	def __init__(self, logFile, logDebug = False):
		if isinstance(self.logger, MainLogger):
			raise RuntimeError("MainLogger has been already created")

		self.logger = self
		utime(self.logFile)
		self.logFile = logFile
		self.logDebug = logDebug
		self.logStream = Thread()
		self.start()

	def getLogger(self):
		return self.logger

	def critical(self, message, **kwargs):
		self.send(message, LogLevel.CRITICAL, "CRITICAL", TextFormat.RED)

	def error(self, message, **kwargs):
		self.send(message, LogLevel.ERROR, "ERROR", TextFormat.DARK_RED)

	def warning(self, message, **kwargs):
		self.send(message, LogLevel.WARNING, "WARNING", TextFormat.YELLOW)

	def info(self, message, **kwargs):
		self.send(message, LogLevel.INFO, "INFO", TextFormat.WHITE)

	def debug(self, message, **kwargs):
		if not self.logDebug:
			return
		self.send(message, LogLevel.DEBUG, "DEBUG", TextFormat.GRAY)

	def setLogDebug(self, logDebug):
		self.logDebug = bool(logDebug)

	def logException(self, e: BaseException, trace = None):
		_type, _value, _tb = sys.exc_info()
		if trace is None:
			trace = traceback.TracebackException(_type, _value, _tb)

		errstr = e
		errfile = trace.filename
		errnum = logging.getLogger().level
		errline = trace.lineno

		errorConversion = {
			logging.CRITICAL: "CRITICAL",
			logging.ERROR:    "ERROR",
			logging.WARNING:  "WARNING",
			logging.INFO:     "INFO",
			logging.DEBUG:    "DEBUG",
			logging.NOTSET:   "NOTSET",
			}
		if errnum == 0:
			_type = 'notset'
		else:
			if errnum == LogLevel.CRITICAL:
				_type = 'critical'
			elif errnum == LogLevel.WARNING:
				_type = 'warning'
			elif errnum == LogLevel.ERROR:
				_type = 'error'
			elif errnum == LogLevel.INFO:
				_type = 'info'
			elif errnum == LogLevel.DEBUG:
				_type = 'debug'

		errnum = isset(errorConversion[errnum]) if errorConversion[errnum] else errnum
		errstr = sub('/\s+/', ' ', str(errstr).trip())
		errfile = PyMine.cleanPath(errfile)
		self.log(_type, type(e).__name__ + ": {} ({}) in {} at line {}".format(errstr, errno, errfile, errline))

		for i, line in PyMine.getTrace(0, trace):
			self.debug(line)
	def log(self, level, message, **kwargs):
		if level == LogLevel.CRITICAL:
			self.critical(message)
		elif level == LogLevel.WARNING:
			self.warning(message)
		elif level == LogLevel.ERROR:
			self.error(message)
		elif level == LogLevel.INFO:
			self.info(message)
		elif level == LogLevel.DEBUG:
			self.debug(message)

	def shutdown(self):
		self.isShutdown = True

	def send(self, message, level, prefix, color):
		now = time.time()
		thread = current_thread()
		if thread is None:
			threadName = "Server thread"
		elif isinstance(thread, Thread) or isinstance(thread, Worker):
			threadName = thread.getThreadName() + " thread"
		else:
			threadName = thread.name  + " thread"

		message = TextFormat.toANSI(TextFormat.AQUA + "[{}]".format(date(now)) + TextFormat.RESET + color + "[{}/{}]:".format(threadName, prefix) + " " + message + TextFormat.RESET)
		cleanMessage = TextFormat.clean(message)

		if not Terminal