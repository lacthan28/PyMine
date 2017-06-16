# -*- coding: utf-8 -*-
from pymine.level.format.SubChunk import SubChunk
from spl.stubs.Core import str_repeat


class EmptySubChunk(SubChunk):
	def __init__(self):
		pass

	def isEmpty(self) -> bool:
		return True

	def getBlockId(self, x: int, y: int, z: int) -> int:
		return 0

	def setBlockId(self, x: int, y: int, z: int, _id: int) -> bool:
		return False

	def getBlockData(self, x: int, y: int, z: int) -> int:
		return 0

	def setBlockData(self, x: int, y: int, z: int, data: int) -> bool:
		return False

	def getFullBlock(self, x: int, y: int, z: int) -> int:
		return 0

	def setBlock(self, x: int, y: int, z: int, _id = None, data = None) -> bool:
		return False

	def getBlockLight(self, x: int, y: int, z: int) -> int:
		return 0

	def setBlockLight(self, x: int, y: int, z: int, level: int) -> bool:
		return False

	def setBlockSkyLight(self, x: int, y: int, z: int, level: int) -> int:
		return 15

	def getBlockIdColumn(self, x: int, z: int) -> str:
		return "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

	def getBlockDataColumn(self, x: int, z: int) -> str:
		return "\x00\x00\x00\x00\x00\x00\x00\x00"

	def getBlockLightColumn(self, x: int, z: int) -> str:
		return "\xff\xff\xff\xff\xff\xff\xff\xff"

	def getBlockIdArray(self) -> str:
		return str_repeat("\x00", 4096)

	def getBlockDataArray(self) -> str:
		return str_repeat("\x00", 2048)

	def getBlockLightArray(self) -> str:
		return str_repeat("\x00", 2048)

	def getSkyLightArray(self) -> str:
		return str_repeat("\xff", 2048)

	def networkSerialize(self) -> str:
		return "\x00" + str_repeat("\x00", 10240)

	def fastSerialize(self) -> str:
		raise BaseException("Should not try to serialize empty subchunks")
