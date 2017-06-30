# -*- coding: utf-8 -*-
from pymine.command.Command import Command
from pymine.command.CommandSender import CommandSender
from pymine.command.defaults.VanillaCommand import VanillaCommand
from pymine.event.TranslationContainer import TranslationContainer


class StopCommand(VanillaCommand):
	def __init__(self, name):
		VanillaCommand.__init__(
				self,
				name,
				"%pymine.command.stop.description",
				"%commands.stop.usage"
				)
		self.setPermission("pymine.command.stop")

	def execute(self, sender: CommandSender, currentAlias, args: dict):
		if not self.testPermission(sender):
			return True

		Command.broadcastCommandMessage(sender, TranslationContainer("commands.stop.start"))

		sender.getServer().shutdown()

		return True
