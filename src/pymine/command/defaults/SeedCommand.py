# -*- coding: utf-8 -*-
from pymine.Player import Player
from pymine.command.CommandSender import CommandSender
from pymine.command.defaults.VanillaCommand import VanillaCommand
from pymine.event.TranslationContainer import TranslationContainer


class SeedCommand(VanillaCommand):
	def __init__(self, name):
		VanillaCommand.__init__(
				self,
				name,
				"%pymine.command.seed.description",
				"%commands.seed.usage")
		self.setPermission('pymine.command.seed')

	def execute(self, sender: CommandSender, currentAlias, args: dict):
		if not self.testPermission(sender):
			return True

		if isinstance(sender, Player):
			seed = sender.getLevel().getSeed()
		else:
			seed = sender.getServer().getDefaultLevel().getSeed()

		sender.sendMessage(TranslationContainer("commands.seed.success", [seed]))
		return True
