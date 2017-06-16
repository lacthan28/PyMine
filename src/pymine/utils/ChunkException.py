# -*- coding: utf-8 -*-

class ChunkException(BaseException):
	def __init__(self, string):
		raise BaseException("Invalid subchunk index " + string + "!")
