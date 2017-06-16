# -*- coding: utf-8 -*-
from pymine.event.Timings import *
from .Task import *
from ..event.TimingsHandler import *


class TaskHandler:
	"""
	:param Task task:
	:param int taskId:
	:param int delay:
	:param int period:
	:param int nextRun:
	:param bool cancelled:
	:param TimingsHandler timings:
	"""

	task = None
	taskId = None
	delay = None
	period = None
	nextRun = None
	cancelled = False
	timings = None
	timingName = None

	def __init__(self, timingName, task: Task, taskId, delay = -1, period = -1):
		"""

		:param str timingName:
		:param Task task:
		:param int taskId:
		:param int delay:
		:param int period:
		"""

		self.task = task
		self.taskId = taskId
		self.delay = delay
		self.period = period
		self.timingName = timingName is None if 'Unknown' else timingName
		self.timings = Timings.getPluginTaskTimings(self, period)
		self.task.setHandler(self)

	def isCancelled(self):
		"""
		:rtype: bool
		:return: True | False
		"""
		return self.cancelled is True

	def getNextRun(self):
		"""
		:rtype: int
		:return: nextRun
		"""
		return self.nextRun

	def setNextRun(self, ticks):
		"""

		:param int ticks:
		"""
		self.nextRun = ticks

	def getTask(self):
		"""
		:rtype: Task
		:return: task
		"""
		return self.task

	def getTaskId(self):
		"""
		:rtype: int
		:return: taskId
		"""
		return self.taskId

	def getDelay(self):
		"""
		:rtype: int
		:return: delay
		"""
		return self.delay

	def isDelayed(self):
		"""
		:rtype: bool
		:return: True | False
		"""
		return self.delay > 0

	def isRepeating(self):
		"""
		:rtype: bool
		:return: True | False
		"""
		return self.period > 0

	def getPeriod(self):
		"""
		:rtype: int
		:return: period
		"""
		return self.period

	def cancel(self):
		"""
		WARNING: Do not use this, it's only for internal use.
		Changes to this function won't be recorded on the version.
		:return:
		"""
		if not self.isCancelled():
			self.task.onCancel()

		self.remove()

	def remove(self):
		self.cancelled = True
		self.task.setHandler(None)

	def run(self, currentTick):
		"""

		:param int currentTick:
		:return:
		"""
		self.task.onRun(currentTick)

	def getTaskName(self):
		"""
		:rtype: str
		:return: timingName
		"""
		if self.timingName is not None:
			return self.timingName
		return type(self.task).__name__
