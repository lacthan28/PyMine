# -*- coding: utf-8 -*-
from abc import ABCMeta
from math import *

from pymine.Player import Player
from pymine.event.Timings import Timings
from pymine.level.Level import Level
from pymine.level.Location import Location
from pymine.maths.AxisAlignedBB import AxisAlignedBB
from pymine.maths.Vector3 import Vector3
from pymine.metadata.Metadatable import Metadatable
from pymine.nbt.tag.CompoundTag import CompoundTag
from pymine.nbt.tag.FloatTag import FloatTag
from spl.stubs.Core import isset, is_array


class Entity(metaclass = ABCMeta, Location, Metadatable):
	NETWORK_ID = -1

	DATA_TYPE_BYTE = 0
	DATA_TYPE_SHORT = 1
	DATA_TYPE_INT = 2
	DATA_TYPE_FLOAT = 3
	DATA_TYPE_STRING = 4
	DATA_TYPE_SLOT = 5
	DATA_TYPE_POS = 6
	DATA_TYPE_LONG = 7
	DATA_TYPE_VECTOR3F = 8

	DATA_FLAGS = 0
	# 1 (int)
	DATA_VARIANT = 2  # int

	DATA_COLOUR = 3  # byte

	DATA_NAMETAG = 4  # string

	DATA_OWNER_EID = 5  # long

	DATA_AIR = 7  # short

	DATA_POTION_COLOR = 8  # int(ARGB!)

	DATA_POTION_AMBIENT = 9  # byte

	DATA_SHOW_NAMETAG = 15

	# 27(byte) player - specific flags
	# 28(int) player "index"?
	# 29(block coords) bed position



	DATA_LEAD_HOLDER_EID = 38
	DATA_LEAD_HOLDER = 38  # long

	DATA_SCALE = 39  # float

	DATA_INTERACTIVE_TAG = 40  # string(button text)
	"""41(long) """

	DATA_URL_TAG = 43  # string

	DATA_MAX_AIR = 44  # short

	DATA_MARK_VARIANT = 45  # int

	"""
	46(byte)
	47(int)
	48(int)
	49(long)
	50(long)
	51(long)
	52(short)
	53(unknown)
	"""

	DATA_BOUNDING_BOX_WIDTH = 54  # float

	DATA_BOUNDING_BOX_HEIGHT = 55  # float

	DATA_FUSE_LENGTH = 56  # int

	DATA_RIDE_POSITION = 57  # vector3f
	"""
	58(byte)
	59(float)
	60(float)
	"""

	DATA_AREA_EFFECT_CLOUD_RADIUS = 61  # float

	DATA_AREA_EFFECT_CLOUD_WAITING = 62  # int

	DATA_AREA_EFFECT_CLOUD_PARTICLE_ID = 63  # int
	"""
	64(int), shulker - related
	65(byte), shulker - related
	66(short)
	shulker - related
	67(unknown), shulker - related
	"""

	DATA_TRADING_PLAYER_EID = 68  # long

	DATA_FLAG_ONFIRE = 0

	DATA_FLAG_SNEAKING = 1

	DATA_FLAG_RIDING = 2

	DATA_FLAG_SPRINTING = 3

	DATA_FLAG_ACTION = 4

	DATA_FLAG_INVISIBLE = 5

	DATA_FLAG_TEMPTED = 6  # ???

	DATA_FLAG_INLOVE = 7

	DATA_FLAG_SADDLED = 8

	DATA_FLAG_POWERED = 9

	DATA_FLAG_IGNITED = 10  # for creepers?

	DATA_FLAG_BABY = 11

	DATA_FLAG_CONVERTING = 12  # ???

	DATA_FLAG_CRITICAL = 13

	DATA_FLAG_CAN_SHOW_NAMETAG = 14

	DATA_FLAG_ALWAYS_SHOW_NAMETAG = 15

	DATA_FLAG_IMMOBILE = 16
	DATA_FLAG_NO_AI = 16

	DATA_FLAG_SILENT = 17

	DATA_FLAG_WALLCLIMBING = 18

	DATA_FLAG_RESTING = 19  # for bats?

	DATA_FLAG_SITTING = 20

	DATA_FLAG_ANGRY = 21

	DATA_FLAG_INTERESTED = 22  # for mobs following players with food?

	DATA_FLAG_CHARGED = 23

	DATA_FLAG_TAMED = 24

	DATA_FLAG_LEASHED = 25

	DATA_FLAG_SHEARED = 26  # for sheep

	DATA_FLAG_GLIDING = 27
	DATA_FLAG_FALL_FLYING = 27

	DATA_FLAG_ELDER = 28  # elder guardian

	DATA_FLAG_MOVING = 29

	DATA_FLAG_BREATHING = 30  # hides bubbles if True

	DATA_FLAG_CHESTED = 31  # for mules?

	DATA_FLAG_STACKABLE = 32

	DATA_FLAG_IDLING = 36

	entityCount = 1
	""":type list:"""
	knownEntities = []
	shortNames = []

	@staticmethod
	def init():
		Entity.registerEntity(Arrow)
		Entity.registerEntity(Item)
		Entity.registerEntity(FallingSand)
		Entity.registerEntity(PrimedTNT)
		Entity.registerEntity(FishingHook)
		Entity.registerEntity(Snowball)
		Entity.registerEntity(Villager)
		Entity.registerEntity(Zombie)
		Entity.registerEntity(Squid)
		Entity.registerEntity(Horse)
		Entity.registerEntity(Human, True)
		Entity.registerEntity(Bat)
		Entity.registerEntity(Blaze)
		Entity.registerEntity(Boat)
		Entity.registerEntity(CaveSpider)
		Entity.registerEntity(Chicken)
		Entity.registerEntity(Cow)
		Entity.registerEntity(Creeper)
		Entity.registerEntity(Egg)
		Entity.registerEntity(EnderPearl)
		Entity.registerEntity(Enderman)
		Entity.registerEntity(ElderGuardian)
		Entity.registerEntity(Ghast)
		Entity.registerEntity(Guardian)
		Entity.registerEntity(Husk)
		Entity.registerEntity(IronGolem)
		Entity.registerEntity(MagmaCube)
		Entity.registerEntity(Ocelot)
		Entity.registerEntity(Pig)
		Entity.registerEntity(PigZombie)
		Entity.registerEntity(Rabbit)
		Entity.registerEntity(Sheep)
		Entity.registerEntity(Spider)
		Entity.registerEntity(Silverfish)
		Entity.registerEntity(Skeleton)
		Entity.registerEntity(Slime)
		Entity.registerEntity(SnowGolem)
		Entity.registerEntity(Wither)
		Entity.registerEntity(Wolf)
		Entity.registerEntity(Witch)
		Entity.registerEntity(Mule)
		Entity.registerEntity(Donkey)
		Entity.registerEntity(SkeletonHorse)
		Entity.registerEntity(ZombieHorse)
		Entity.registerEntity(Stray)
		Entity.registerEntity(WitherSkeleton)
		Entity.registerEntity(Minecart)
		Entity.registerEntity(Mooshroom)
		Entity.registerEntity(ThrownPotion)
		Entity.registerEntity(ThrownExpBottle)
		Entity.registerEntity(XPOrb)
		Entity.registerEntity(Lightning)
		Entity.registerEntity(EnderDragon)
		Entity.registerEntity(Endermite)
		Entity.registerEntity(PolarBear)
		Entity.registerEntity(Shulker)

	hasSpawned = []

	effects = []

	_id = None

	dataFlags = 0

	dataProperties = {
		DATA_FLAGS:           [DATA_TYPE_LONG, 0],
		DATA_AIR:             [DATA_TYPE_SHORT, 400],
		DATA_MAX_AIR:         [DATA_TYPE_SHORT, 400],
		DATA_NAMETAG:         [DATA_TYPE_STRING, ""],
		DATA_LEAD_HOLDER_EID: [DATA_TYPE_LONG, -1],
		DATA_SCALE:           [DATA_TYPE_FLOAT, 1],
		}

	passenger = None
	vehicle = None

	chunk = None

	lastDamageCause = None

	blocksAround = []

	lastX = None
	lastY = None
	lastZ = None

	motionX = None
	motionY = None
	motionZ = None

	temporalVector = None
	lastMotionX = None
	lastMotionY = None
	lastMotionZ = None

	lastYaw = None
	lastPitch = None
	lastHeadYaw = None

	prevRenderYawOffset = 0
	renderYawOffset = 0

	headYaw = 0

	boundingBox = None
	onGround = None
	inBlock = False
	positionChanged = None
	motionChanged = None
	deadTicks = 0
	age = 0

	height = None

	eyeHeight = None

	width = None
	length = None

	health = 20
	maxHealth = 20

	ySize = 0
	stepHeight = 0
	keepMovement = False

	fallDistance = 0
	ticksLived = 0
	lastUpdate = None
	maxFireTicks = None
	fireTicks = 0
	namedtag = None
	canCollide = True

	isStatic = False

	isCollided = False
	isCollidedHorizontally = False
	isCollidedVertically = False

	noDamageTicks = None
	justCreated = None
	invulnerable = None

	attributeMap = None

	gravity = None
	drag = None

	server = None

	closed = False

	timings = None
	isPlayer = False

	ridingEntity = None

	def __init__(self, level: Level, nbt: CompoundTag):
		self.timings = Timings.getEntityTimings(self)

		self.isPlayer = isinstance(self, Player)

		self.temporalVector = Vector3()

		if self.eyeHeight is None:
			self.eyeHeight = self.height / 2 + 0.1

		self._id = Entity.entityCount + 1
		self.justCreated = True
		self.namedtag = nbt

		self.chunk = level.getChunk(self.namedtag["Pos"][0] >> 4, self.namedtag["Pos"][2] >> 4)
		assert self.chunk is not None
		self.setLevel(level)
		self.server = level.getServer()

		self.boundingBox = AxisAlignedBB(0, 0, 0, 0, 0, 0)
		self.setPositionAndRotation(
				self.temporalVector.setComponents(
						self.namedtag["Pos"][0],
						self.namedtag["Pos"][1],
						self.namedtag["Pos"][2]
						),
				self.namedtag.Rotation[0],
				self.namedtag.Rotation[1]
				)
		self.setMotion(
				self.temporalVector.setComponents(
						self.namedtag["Motion"][0],
						self.namedtag["Motion"][1],
						self.namedtag["Motion"][2]
						)
				)

		assert not isnan(self.x) and not isinf(self.x) and not isnan(self.y) and not isinf(self.y) and not isnan(
				self.z) and not isinf(self.z)

		if not isset(self.namedtag.FallDistance):
			self.namedtag.FallDistance = FloatTag("FallDistance", 0)

		self.fallDistance = self.namedtag["FallDistance"]

		if not isset(self.namedtag.Fire):
			self.namedtag.FallDistance = FloatTag("Fire", 0)

		self.fireTicks = self.namedtag["Fire"]

	def getId(self):
		pass

	def initEntity(self):
		assert isinstance(self.namedtag, CompoundTag)

		if isset(self.namedtag.CustomName):
			self.setNameTag(self.namedtag["CustomName"])
			if isset(self.namedtag.CustomNameVisible):
				self.setNameTagVisible(self.namedtag["CustomNameVisible"] > 0)

		self.scheduleUpdate()
		self.addAttributes()

		if isset(self.namedtag.ActiveEffects):
			for e in self.namedtag.ActiveEffects.getValue():
				amplifier = e["Amplifier"] & 0xff

				effect = Effect.getEffect(e["Id"])
				if effect is None:
					continue
				effect.setAmplifier(amplifier).setDuration(e["Duration"]).setVisible(e["ShowParticles"] > 0)

				self.addEffect(effect)

	def addAttributes(self):
		pass

	def scheduleUpdate(self):
		self.level.updateEntities[self._id] = self

	def setNameTag(self, name):
		self.setDataProperty(Entity.DATA_NAMETAG, Entity.DATA_TYPE_STRING, name)

	def setDataProperty(self, _id, _type, value, send = True):
		if self.getDataProperty(_id) != value:
			self.dataProperties[_id] = [_type, value]
			if send is True:
				self.sendData(self.hasSpawned, { _id: self.dataProperties[_id] })

			return True
		return False

	def getDataProperty(self, _id):
		return isset(self.dataProperties[_id]) if self.dataProperties[_id][1] else None

	def sendData(self, player, data = None):
		import copy
		if not is_array(player):
			player = [player]

		pk = SetEntityDataPacket()
		pk.eid = self.getId()
		pk.metadata = data is None if self.dataProperties else data

		for p in player:
			if p is self:
				continue
			p.dataPacket(copy.copy(pk))
		if isinstance(self, Player):
			self.dataPacket(pk)
