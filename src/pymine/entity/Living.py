# -*- coding: utf-8 -*-
from abc import ABCMeta

from pymine.entity.Damageable import Damageable
from pymine.entity.Entity import Entity


class Living(metaclass = ABCMeta, Entity, Damageable):
	gravity = 0.08
	drag = 0.02

	attackTime = 0

	invisible = False

	navigator = None
	tasks = None
	targetTasks = None
	lookHelper = None
	moveHelper = None
	jumpHelper = None

	isJumping = False
	jumpMovementFactor = 0.02
	jumpTicks = 0

	moveForward = 0.0
	moveStrafing = 0.0
	landMovementFactor = None
	attackTarget = None
	entityLivingToAttack = None
	revengeTimer = -1
	recentlyHit = 0
	attackingPlayer = None

	def initEntity(self):
		Entity.initEntity()

