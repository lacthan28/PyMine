# -*- coding: utf-8 -*-
from .ThreadedLoggerAttachment import *
from .ThreadedLogger import *


class AttachableThreadedLogger(ThreadedLogger):
	"""
	:param ThreadedLoggerAttachment attachment:
	"""
	attachment = None

	def addAttachment(self, attachment: ThreadedLoggerAttachment):
		"""

		:param ThreadedLoggerAttachment attachment:
		:return:
		"""
		if isinstance(self.attachment, ThreadedLoggerAttachment):
			self.attachment.addAttachment(attachment)
		else:
			self.attachment = attachment

	def removeAttachment(self, attachment: ThreadedLoggerAttachment):
		"""

		:param ThreadedLoggerAttachment attachment:
		:return:
		"""
		if isinstance(self.attachment, ThreadedLoggerAttachment):
			if self.attachment == attachment:
				self.attachment = None
				for attachment in attachment.getAttachments():
					self.addAttachment(attachment)

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
