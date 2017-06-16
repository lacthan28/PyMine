# -*- coding: utf-8 -*-
from abc import *
from .TaskHandler import *


class Task(metaclass = ABCMeta):
	"""
	WARNING! Plugins that create tasks MUST extend PluginTask

	:param TaskHandler taskHandler:
	"""

	taskHandler = None

	def getHandler(self):
		"""
		:rtype: TaskHandler
		:return:
		"""
		return self.taskHandler

	def getTaskId(self):
		"""
		:rtype int
		:return:
		"""
		if self.taskHandler is not None:
			return self.taskHandler.getTaskId()

		return -1

	def setHandler(self, taskHandler):
		"""
		:param TaskHandler|None taskHandler:
		:return:
		"""
		if self.taskHandler is None or taskHandler is None:
			self.taskHandler = taskHandler

	@abstractmethod
	def onRun(self, currentTicks):
		"""
		Actions to execute when run

		:param currentTicks:
		:return:
		"""
		pass

	def onCancel(self):
		"""
		Actions to execute if the Task is cancelled

		:return:
		"""
		pass
