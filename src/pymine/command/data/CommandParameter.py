# -*- coding: utf-8 -*-

class CommandParameter:
	ARG_TYPE_STRING = "string"
	ARG_TYPE_STRING_ENUM = "stringenum"
	ARG_TYPE_BOOL = "bool"
	ARG_TYPE_TARGET = "target"
	ARG_TYPE_PLAYER = "target"
	ARG_TYPE_BLOCK_POS = "blockpos"
	ARG_TYPE_RAW_TEXT = "rawtext"
	ARG_TYPE_INT = "int"
	ARG_TYPE_TARGET_ALL_PLAYERS = "allPlayers"  # @a
	ARG_TYPE_TARGET_ALL_ENTITIES = "allEntities"  # @e
	ARG_TYPE_TARGET_NEAREST_PLAYER = "nearestPlayer"  # @n
	ARG_TYPE_TARGET_RANDOM_PLAYER = "randomPlayer"  # @r

	name = None
	varType = None
	optional = None

	def __init__(self, name, varType = ARG_TYPE_RAW_TEXT, optional = False):
		self.name = name
		self.varType = varType
		self.optional = optional
