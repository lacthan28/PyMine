# -*- coding: utf-8 -*-
from abc import *


class Logger(metaclass = ABCMeta):
	def emergency(self, message):
		pass

	def alert(self, message):
		pass

	def critical(self, message):
		pass

	def error(self, message):
		pass

	def warning(self, message):
		pass

	def notice(self, message):
		pass

	def info(self, message):
		pass

	def debug(self, message):
		pass

	def log(self, level, message):
		pass

	def logException(self, e: BaseException, trace = None):
		pass
