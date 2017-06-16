# -*- coding: utf-8 -*-
from pymine.Player import Player
from pymine.block.Block import Block
from pymine.entity.Entity import Entity
from pymine.level.format.EmptySubChunk import *
from pymine.level.format.io.ChunkException import *
from pymine.tile.Tile import Tile
from spl.stubs.Core import isset, str_repeat


class Chunk:
	"""
	:param SubChunk[] subChunks:

	:param EmptySubChunk emptySubChunk:

	:param Tile[] tiles:
	:param Tile[] tileList:

	:param Entity[] entities:

	:param int[256] heightMap:

	:param str biomeIds:

	:param CompoundTag[] NBTtiles;
	:param CompoundTag[] NBTentities;

	"""
	MAX_SUBCHUNKS = 16

	x = None
	z = None

	hasChanged = False

	isInit = False

	lightPopulated = False
	terrainGenerated = False
	terrainPopulated = False

	height = MAX_SUBCHUNKS

	subChunks = { }

	emptySubChunk = None

	tiles = { }
	tileList = { }

	entities = { }

	heightMap = { }

	biomeIds = None

	extraData = { }

	NBTtiles = { }

	NBTentities = { }

	def __init__(self, chunkX: int, chunkZ: int, subChunks = None, entities = None, tiles = None,
	             biomeIds: str = "", heightMap = None):
		"""

		:param int chunkX:
		:param int chunkZ:
		:param dict subChunks: SubChunk[]
		:param dict entities: CompoundTag[]
		:param dict tiles: CompoundTag[]
		:param str biomeIds:
		:param dict heightMap: int[]
		"""
		if heightMap is None:
			heightMap = { }
		if tiles is None:
			tiles = { }
		if entities is None:
			entities = { }
		if subChunks is None:
			subChunks = { }

		self.x = chunkX
		self.z = chunkZ

		self.height = Chunk.MAX_SUBCHUNKS  # TODO: add a way of changing this

		self.emptySubChunk = EmptySubChunk()

		for y, subChunk in subChunks:
			if y < 0 or y >= self.height:
				raise ChunkException(y)

			if subChunk.isEmpty():
				self.subChunks[y] = self.emptySubChunk
			else:
				self.subChunks[y] = subChunk

		for i in range(self.height):
			if not isset(self.subChunks[i]):
				self.subChunks[i] = self.emptySubChunk

		if len(heightMap) == 256:
			self.heightMap = heightMap
		else:
			assert len(heightMap) == 0, "Wrong HeightMap value count, expected 256, got " + str(len(heightMap))
			val = (self.height * 16) - 1
			self.heightMap = [val for i in range(256)]

		if len(biomeIds) == 256:
			self.biomeIds = biomeIds
		else:
			assert len(biomeIds) == 0, "Wrong BiomeIds value count, expected 256, got " + str(len(biomeIds))
			self.biomeIds = str_repeat("\x00", 256)

		self.NBTtiles = tiles
		self.NBTentities = entities

	def getX(self) -> int:
		"""
		:rtype: int
		:return: x
		"""
		return self.x

	def getZ(self) -> int:
		"""
		:rtype: int
		:return: z
		"""
		return self.z

	def setX(self, x: int):
		"""

		:param int x:
		:return:
		"""
		self.x = x

	def setZ(self, z: int):
		"""

		:param int z:
		:return:
		"""
		self.z = z

	def getHeight(self) -> int:
		"""
		:rtype: int
		:return: height
		"""
		return self.height

	def getFullBlock(self, x: int, y: int, z: int) -> int:
		"""
		Returns a bitmap of block ID and meta at the specified chunk block coordinates
		:param int x: 0-15
		:param int y:
		:param int z: 0-15
		:rtype: int
		:rtype: int
		:returns: int bitmap, (id << 4) | meta
		"""
		return self.getSubChunk(y >> 4).getFullBlock(x, y & 0x0f, z)

	def setBlock(self, x: int, y: int, z: int, blockId = None, meta = None) -> bool:
		"""
		Sets block ID and meta in one call at the specified chunk block coordinates
		:param int x: 0-15
		:param int y:
		:param int z: 0-15
		:param int|None blockId: 0-255 if null, does not change
		:param int|None meta: 0-15 if null, does not change
		:rtype: bool
		:return:
		"""
		if self.getSubChunk(y >> 4, True).setBlock(x, y & 0x0f, z, blockId is not None if (blockId & 0xff) else None,
		                                           meta is not None if (meta & 0x0f)else None):
			self.hasChanged = True
			return True
		return False

	def getBlockId(self, x: int, y: int, z: int) -> int:
		"""
		Returns the block ID at the specified chunk block coordinates
		:param int x: 0-15
		:param int y:
		:param int z: 0-15
		:rtype: int
		:return: 0-255
		"""
		return self.getSubChunk(y >> 4).getBlockId(x, y & 0x0f, z)

	def setBlockId(self, x: int, y: int, z: int, _id: int):
		"""
		Returns the block ID at the specified chunk block coordinates
		:param int x: 0-15
		:param int y:
		:param int z: 0-15
		:param int _id: 0-255
		"""
		if self.getSubChunk(y >> 4, True).setBlockId(x, y & 0x0f, z, _id):
			self.hasChanged = True

	def getBlockData(self, x: int, y: int, z: int) -> int:
		"""
		Returns the block meta value at the specified chunk block coordinates
		:param int x: 0-15
		:param int y:
		:param int z: 0-15
		:rtype: int
		:return: 0-15
		"""
		return self.getSubChunk(y >> 4).getBlockData(x, y & 0x0f, z)

	def setBlockData(self, x: int, y: int, z: int, data: int):
		"""
		Sets the block meta value at the specified chunk block coordinates
		:param int x: 0-15
		:param int y:
		:param int z: 0-15
		:param int data: 0-15
		"""
		if self.getSubChunk(y >> 4).setBlockData(x, y & 0x0f, z, data):
			self.hasChanged = True

	def getBlockExtraData(self, x: int, y: int, z: int) -> int:
		"""
		Returns the raw block extra data value at the specified chunk block coordinates, or 0 if no data exists
		:param int x: 0-15
		:param int y:
		:param int z: 0-15
		:rtype: int
		:return: bitmap, (meta << 8) | id
		"""
		return self.extraData[Chunk.chunkBlockHash(x, y, z)] if self.extraData[Chunk.chunkBlockHash(x, y, z)] else 0

	def setBlockExtraData(self, x: int, y: int, z: int, data: int):
		"""
		Sets the raw block extra data value at the specified chunk block coordinates
		:param int data: bitmap, (meta << 8) | id
		:param int x: 0-15
		:param int y:
		:param int z: 0-15
		"""
		if data == 0:
			del self.extraData[Chunk.chunkBlockHash(x, y, z)]
		else:
			self.extraData[Chunk.chunkBlockHash(x, y, z)] = data

		self.hasChanged = True

	def getBlockSkyLight(self, x: int, y: int, z: int) -> int:
		"""
		Returns the sky light level at the specified chunk block coordinates
		:param int x: 0-15
		:param int y:
		:param int z: 0-15
		:rtype: int
		:return: 0-15
		"""
		return self.getSubChunk(y >> 4).getBlockSkyLight(x, y & 0x0f, z)

	def setBlockSkyLight(self, x: int, y: int, z: int, level: int):
		"""
		Sets the sky light level at the specified chunk block coordinates
		:param int x: 0-15
		:param int y:
		:param int z: 0-15
		:param int level: 0-15
		:return:
		"""
		if self.getSubChunk(y >> 4).setBlockSkyLight(x, y & 0x0f, z, level):
			self.hasChanged = True

	def getBlockLight(self, x: int, y: int, z: int) -> int:
		"""
		Returns the block light level at the specified chunk block coordinates
		:param int x: 0-15
		:param int y: 0-15
		:param int z: 0-15
		:rtype: int
		:return: 0-15
		"""
		return self.getSubChunk(y >> 4).getBlockLight(x, y & 0x0f, z)

	def setBlockLight(self, x: int, y: int, z: int, level: int):
		"""
		Sets the block light level at the specified chunk block coordinates
		:param int x: 0-15
		:param int y: 0-15
		:param int z: 0-15
		:param int level: 0-15
		:return:
		"""
		if self.getSubChunk(y >> 4).setBlockLight(x, y & 0x0f, z, level):
			self.hasChanged = True

	def getHighestBlockAt(self, x: int, z: int, useHeightMap: bool = True) -> int:
		"""
		Returns the Y coordinate of the highest non-air block at the specified X/Z chunk block coordinates
		:param int x: 0-15
		:param int z: 0-15
		:param bool useHeightMap: whether to use pre-calculated heightmap values or not
		:rtype: int
		:return:
		"""
		if useHeightMap:
			height = self.getHeightMap(x, z)
			if height != 0 and height != 255:
				return height

		index = self.getHighestSubChunkIndex()
		if index < 0:
			return 0

		height = index << 4
		for y in range(index):
			height = self.getSubChunk(y).getHighestBlockAt(x, z) | (y << 4)
			if height != -1:
				break

		self.setHeightMap(x, z, height)
		return height

	def getHeightMap(self, x: int, z: int) -> int:
		"""
		Returns the heightmap value at the specified X/Z chunk block coordinates
		:param int x: 0-15
		:param int z: 0-15
		:rtype: int
		:return:
		"""
		return self.heightMap[(z << 4) | x]

	def setHeightMap(self, x: int, z: int, value: int):
		"""
		Sets the heightmap value at the specified X/Z chunk block coordinates
		:param int x: 0-15
		:param int z: 0-15
		:param int value:
		:return:
		"""
		self.heightMap[(z << 4) | x] = value

	def recalculateHeightMap(self):
		"""
		Recalculates the heightmap for the whole chunk.
		:return:
		"""
		for z in range(16):
			for x in range(16):
				self.setHeightMap(x, z, self.getHighestBlockAt(x, z, False))

	def populateSkyLight(self):
		"""
		Performs basic sky light population on the chunk.
		:return:
		"""
		# TODO: rewrite this, use block light filters and diffusion, actual proper sky light population

		for x in range(16):
			for z in range(16):
				heightMap = self.getHeightMap(x, z)
				y = (self.getHighestSubChunkIndex() + 1) << 4

				# TODO: replace a section of the array with a string in one call to improve performance
				while y > heightMap:
					self.setBlockSkyLight(x, y, z, 15)
					y -= 1
				while y > 0 and self.getBlockId(x, y, z) == Block.AIR:
					self.setBlockSkyLight(x, y, z, 15)
					y -= 1
				self.setHeightMap(x, z, y)

				while y > 0:
					self.setBlockSkyLight(x, y, z, 0)
					y -= 1

	def getBiomeId(self, x: int, z: int) -> int:
		"""
		Returns the biome ID at the specified X/Z chunk block coordinates
		:param int x: 0-15
		:param int z: 0-15
		:return:
		"""
		return ord(self.biomeIds[(z << 4) | x])

	def setBiomeId(self, x: int, z: int, biomeId: int):
		"""
		Sets the biome ID at the specified X/Z chunk block coordinates
		:param int x: 0-15
		:param int z: 0-15
		:param int biomeId: 0-255
		:return:
		"""
		self.hasChanged = True
		self.biomeIds[(z << 4) | x] = chr(biomeId & 0xff)

	def getBlockIdColumn(self, x: int, z: int) -> str:
		"""
		Returns a column of block IDs from bottom to top at the specified X/Z chunk block coordinates.
		:param int x: 0-15
		:param int z: 0-15
		:rtype: str
		:return:
		"""
		result = ''
		for subChunk in self.subChunks:
			result += subChunk.getBlockIdColumn(x, z)

		return result

	def getBlockDataColumn(self, x: int, z: int) -> str:
		"""
		Returns a column of block meta values from bottom to top at the specified X/Z chunk block coordinates.
		:param int x: 0-15
		:param int z: 0-15
		:rtype: str
		:return:
		"""
		result = ''
		for subChunk in self.subChunks:
			result += subChunk.getBlockDataColumn(x, z)

		return result

	def getBlockSkyLightColumn(self, x: int, z: int) -> str:
		"""
		Returns a column of sky light values from bottom to top at the specified X/Z chunk block coordinates.
		:param int x: 0-15
		:param int z: 0-15
		:rtype: str
		:return:
		"""
		result = ''
		for subChunk in self.subChunks:
			result += subChunk.getSkyLightColumn(x, z)

		return result

	def getBlockLightColumn(self, x: int, z: int) -> str:
		"""
		Returns a column of block light values from bottom to top at the specified X/Z chunk block coordinates.
		:param int x: 0-15
		:param int z: 0-15
		:rtype: str
		:return:
		"""
		result = ''
		for subChunk in self.subChunks:
			result += subChunk.getBlockLightColumn(x, z)

		return result

	def isLightPopulated(self) -> bool:
		"""
		:rtype: bool
		:return:
		"""
		return self.lightPopulated

	def setLightPopulated(self, value: bool = True):
		"""

		:param bool value:
		:return:
		"""
		self.lightPopulated = value

	def isPopulated(self) -> bool:
		"""
		:rtype: bool
		:return:
		"""
		return self.terrainPopulated

	def setPopulated(self, value: bool = True):
		"""

		:param bool value:
		:return:
		"""
		self.terrainPopulated = value

	def isGenerated(self) -> bool:
		"""
		:rtype: bool
		:return:
		"""
		return self.terrainGenerated

	def setGenerated(self, value: bool = True):
		"""

		:param bool value:
		:return:
		"""
		self.terrainGenerated = value

	def addEntity(self, entity: Entity):
		"""

		:param Entity entity:
		:return:
		"""
		self.entities[entity.getId()] = entity
		if not isinstance(entity, Player) and self.isInit:
			self.hasChanged = True

	def removeEntity(self, entity: Entity):
		"""

		:param Entity entity:
		:return:
		"""
		del self.entities[entity.getId()]
		if not isinstance(entity, Player) and self.isInit:
			self.hasChanged = True

	def addTile(self, tile: Tile):
		"""

		:param Tile tile:
		:return:
		"""
		self.tiles[tile.getId()] = tile
		index = ((tile.x & 0x0f) << 12) | ((tile.z & 0x0f) << 8) | (tile.y & 0xff)])
		if isset(self.tileList[index])
		if self.isInit:
			self.hasChanged = True

	def getSubChunk(self, y: int, generateNew: bool = False) -> SubChunk:
		"""
		Returns the subchunk at the specified subchunk Y coordinate, or an empty, unmodifiable stub if it does not exist or the coordinate is out of range.
		:param int y:
		:param bool generateNew: Whether to create a new, modifiable subchunk if there is not one in place
		:rtype: SubChunk|EmptySubChunk
		:return: subChunks[y]
		"""
		if y < 0 or y >= self.height:
			return self.emptySubChunk
		elif generateNew and isinstance(self.subChunks[y], EmptySubChunk):
			self.subChunks[y] = SubChunk()

		assert self.subChunks[y] is not None, "Somehow something broke, no such subchunk at index " + str(y)
		return self.subChunks[y]
