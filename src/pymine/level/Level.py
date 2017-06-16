# -*- coding: utf-8 -*-
from pymine.Server import Server
from spl.stubs.Core import isset


class Level:
	"""
	:param Server server:
	"""
	server = None

	def getServer(self) -> Server:
		return self.server

	def getChunk(self, x: int, z: int, create: bool = False):
		index = Level.chunkHash(x, z)
		if isset(self.chunks[index]):
			return self.chunks[index]
		elif self.loadChunk(x, z, create):
			return self.chunks[index]

		return None
