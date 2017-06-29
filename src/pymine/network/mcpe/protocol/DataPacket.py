# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from pymine.utils.BinaryStream import BinaryStream


class DataPacket(metaclass = ABCMeta, BinaryStream):
	NETWORK_ID = 0

	isEncoded = False

	def pid(self):
		return self.NETWORK_ID

	@abstractmethod
	def encode(self):
		pass

	@abstractmethod
	def decode(self):
		pass

	def reset(self):
		self.buffer = chr(self.NETWORK_ID)
		self.offset = 0

	def clean(self):
		self.buffer = None
		self.isEncoded = False
		self.offset = 0
		return self

	def __debugInfo(self):
		data = { }
		for k, v in self:
			if k == "buffer":
				data[k] = hex(v)
			elif isinstance(v, str) or (
					isinstance(v, object) and hasattr(v, "__str__") and callable(getattr(v, "__str__"))):
				data[k] = Utils.printable(str(v))