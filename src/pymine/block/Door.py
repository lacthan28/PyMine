# -*- coding: utf-8 -*-
from abc import *

from pymine.block.Transparent import Transparent
from pymine.maths.AxisAlignedBB import AxisAlignedBB
from pymine.maths.Vector3 import Vector3


class Door(metaclass = ABCMeta, Transparent):
	def canBeActivated(self):
		return True

	def isSolid(self):
		return False

	def getFullDamage(self):
		damage = self.getDamage()
		isUp = (damage & 0x08) > 0
		if isUp:
			down = self.getSide(Vector3.SIDE_DOWN).getDamage()
			up = damage
		else:
			down = damage
			up = self.getSide(Vector3.SIDE_UP).getDamage()

		isRight = (up & 0x01) > 0
		return down & 0x07 | (isUp if 8 else 0) | (isRight if 0x10 else 0)

	def recalculateBoundingBox(self):
		f = 0.1875
		damage = self.getFullDamage()
		bb = AxisAlignedBB(
				self.x,
				self.y,
				self.z,
				self.x + 1,
				self.y + 1,
				self.z + 1
				)

		j = damage & 0x03
		isOpen = ((damage & 0x04) > 0)
		isRight = ((damage & 0x10) > 0)

		if j == 0:
			if isOpen:
				if not isRight:
					bb.setBounds(
							self.x,
							self.y,
							self.z,
							self.x + 1,
							self.y + 1,
							self.z + f
							)
				else:
					bb.setBounds(
							self.x,
							self.y,
							self.z + 1 - f,
							self.x + 1,
							self.y + 1,
							self.z + 1
							)
			else:
				bb.setBounds(
						self.x,
						self.y,
						self.z,
						self.x + f,
						self.y + 1,
						self.z + 1
						)
		elif j == 1:
			if isOpen:
				if not isRight:
					bb.setBounds(
							self.x + 1 -f,
							self.y,
							self.z,
							self.x + 1,
							self.y + 1,
							self.z + 1
							)
				else:
					bb.setBounds(
							self.x,
							self.y,
							self.z,
							self.x + f,
							self.y + 1,
							self.z + 1
							)
			else:
				bb.setBounds(
						self.x,
						self.y,
						self.z,
						self.x + 1,
						self.y + 1,
						self.z + f
						)
