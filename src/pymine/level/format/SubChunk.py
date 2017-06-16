# -*- coding: utf-8 -*-

from spl.stubs.Core import str_repeat, substr

strict_types = 1


class SubChunk:
	ids = None
	data = None
	blockLight = None
	skyLight = None

	@staticmethod
	def assignData(target, data, length, value = '\x00'):
		if len(data) != length:
			assert data == '', "Invalid non-zero length given, expected " + length + ", got " + str(len(data))
			target = str_repeat(value, length)
		else:
			target = data

	def __init__(self, ids: str = "", data: str = "", skyLight: str = "", blockLight: str = ""):
		SubChunk.assignData(self.ids, ids, 4096)
		SubChunk.assignData(self.data, data, 2048)
		SubChunk.assignData(self.skyLight, skyLight, 2048, "\xff")
		SubChunk.assignData(self.blockLight, blockLight, 2048)

	def isEmpty(self) -> bool:
		assert len(self.ids) == 4096, "Wrong length of ID array, expecting 4096 bytes, got " + str(len(self.ids))
		return self.ids.count("\x00") == 4096

	def getBlockId(self, x: int, y: int, z: int) -> int:
		return ord(self.ids[(x << 8) | (z << 4) | y])

	def setBlockId(self, x: int, y: int, z: int, _id: int) -> bool:
		self.ids[(x << 8) | (z << 4) | y] = chr(_id)
		return True

	def getBlockData(self, x: int, y: int, z: int) -> int:
		m = ord(self.data[(x << 7) + (z << 3) + (y >> 1)])
		if (y & 1) == 0:
			return m & 0x0f
		else:
			return m >> 4

	def setBlockData(self, x: int, y: int, z: int, data: int) -> bool:
		i = (x << 7) | (z << 3) | (y >> 1)
		if (y & 1) == 0:
			self.data[i] = chr((ord(self.data[i]) & 0xf0) | (data & 0x0f))
		else:
			self.data[i] = chr(((data & 0x0f) << 4) | (ord(self.data[i]) & 0x0f))

		return True

	def getFullBlock(self, x: int, y: int, z: int) -> int:
		i = (x << 8) | (z << 4) | y
		if (y & 1) == 0:
			return (ord(self.ids[i]) << 4) | (ord(self.data[i >> 1]) & 0x0f)
		else:
			return (ord(self.ids[i]) << 4) | (ord(self.data[i >> 1]) >> 4)

	def setBlock(self, x: int, y: int, z: int, _id = None, data = None) -> bool:
		i = (x << 8) | (z << 4) | y
		changed = False
		if _id is not None:
			block = chr(_id)
			if self.ids[i] != block:
				self.ids[i] = block
				changed = True

		if data is not None:
			i >>= 1
			byte = ord(self.data[i])
			if (y & 1) == 0:
				self.data[i] = chr((byte & 0xf0) | (data & 0x0f))
			else:
				self.data[i] = chr(((data & 0x0f) << 4) | (byte & 0x0f))

			if self.data[i] != byte:
				changed = True

		return changed

	def getBlockLight(self, x: int, y: int, z: int) -> int:
		byte = ord(self.blockLight[(x << 7) + (z << 3) + (y >> 1)])
		if (y & 1) == 0:
			return byte & 0x0f
		else:
			return byte >> 4

	def setBlockLight(self, x: int, y: int, z: int, level: int) -> bool:
		i = (x << 7) + (z << 3) + (y >> 1)
		byte = ord(self.blockLight[i])
		if (y & 1) == 0:
			self.blockLight[i] = chr((byte & 0xf0) | (level & 0x0f))
		else:
			self.blockLight[i] = chr(((level & 0x0f) << 4) | (byte & 0x0f))

		return True

	def getBlockSkyLight(self, x: int, y: int, z: int) -> int:
		byte = ord(self.skyLight[(x << 7) + (z << 3) + (y >> 1)])
		if (y & 1) == 0:
			return byte & 0x0f
		else:
			return byte >> 4

	def setBlockSkyLight(self, x: int, y: int, z: int, level: int) -> bool:
		i = (x << 7) + (z << 3) + (y >> 1)
		byte = ord(self.skyLight[i])
		if (y & 1) == 0:
			self.skyLight[i] = chr((byte & 0xf0) | (level & 0x0f))
		else:
			self.skyLight[i] = chr(((level & 0x0f) << 4) | (byte & 0x0f))
		return True

	def getHighestBlockAt(self, x: int, z: int) -> int:
		for y in range(0, 16):
			if self.ids[(x << 8) | (z << 4) | y] != "\x00":
				return y

		return -1  # highest block not in this subchunk

	def getBlockIdColumn(self, x: int, z: int) -> str:
		return substr(self.ids, ((x << 8) | (z << 4)), 16)

	def getBlockDataColumn(self, x: int, z: int) -> str:
		return substr(self.data, ((x << 7) | (z << 3)), 8)

	def getBlockLightColumn(self, x: int, z: int) -> str:
		return substr(self.blockLight, ((x << 7) | (z << 3)), 8)

	def getSkyLightColumn(self, x: int, z: int) -> str:
		return substr(self.skyLight, ((x << 7) | (z << 3)), 8)

	def getBlockIdArray(self) -> str:
		assert (len(self.ids) == 4096, "Wrong length of ID array, expecting 4096 bytes, got " + str(len(self.ids)))
		return self.ids

	def getBlockDataArray(self) -> str:
		assert (len(self.data) == 2048, "Wrong length of data array, expecting 2048 bytes, got " + str(len(self.data)))
		return self.data

	def getSkyLightArray(self) -> str:
		assert (len(self.skyLight) == 2048,
		        "Wrong length of skylight array, expecting 2048 bytes, got " + str(len(self.skyLight)))
		return self.skyLight

	def getBlockLightArray(self) -> str:
		assert (len(self.blockLight) == 2048,
		        "Wrong length of light array, expecting 2048 bytes, got " + str(len(self.blockLight)))
		return self.blockLight

	def networkSerialize(self) -> str:
		# storage version, ids, data, skylight, blocklight
		return "\x00" + self.ids + self.data + self.skyLight + self.blockLight

	def fastSerialize(self) -> str:
		return self.ids + self.data + self.skyLight + self.blockLight

	@staticmethod
	def fastDeserialize(data: str):
		return SubChunk(
				substr(data, 0, 4096),  # ids
				substr(data, 4096, 2048),  # data
				substr(data, 6144, 2048),  # sky light
				substr(data, 8192, 2048)  # block light
				)
