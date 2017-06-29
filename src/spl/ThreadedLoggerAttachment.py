# -*- coding: utf-8 -*-
from threading import Thread
from .LoggerAttachment import *


class ThreadedLoggerAttachment(Thread, LoggerAttachment):
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

	def removeAttachment(self, ThreadedLoggerAttachment):
		if isinstance(self.attachment, ThreadedLoggerAttachment):
			if self.attachment is ThreadedLoggerAttachment.attachment:
				self.attachment = None
				for ThreadedLoggerAttachment.attachment in ThreadedLoggerAttachment.attachment.getAttachments():
					self.addAttachment(ThreadedLoggerAttachment.attachment)

	def removeAttachments(self):
		if isinstance(self.attachment, ThreadedLoggerAttachment):
			self.attachment.removeAttachments()
			self.attachment = None

	def getAttachments(self):
		attachments = []
		if isinstance(self.attachment, ThreadedLoggerAttachment):
			attachments = self.attachment
			attachments += self.attachment.getAttachments()

		return attachments
