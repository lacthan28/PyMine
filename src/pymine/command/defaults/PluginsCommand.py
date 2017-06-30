# -*- coding: utf-8 -*-
from pymine.command.CommandSender import CommandSender
from pymine.command.defaults.VanillaCommand import VanillaCommand
from pymine.event.TranslationContainer import TranslationContainer
from pymine.utils.TextFormat import TextFormat


class PluginsCommand(VanillaCommand):
	def __init__(self, name):
		VanillaCommand.__init__(
				self,
				name,
				"%pymine.command.plugins.description",
				"%pymine.command.plugins.usage",
				["pl"]
				)
		self.setPermission("pymine.command.plugins")

	def execute(self, sender: CommandSender, currentAlias, args: dict):
		if not self.testPermission(sender):
			return True
		self.sendPluginList(sender)
		return True

	def sendPluginList(self, sender: CommandSender):
		lst = ''
		plugins = sender.getServer().getPluginManager().getPlugins()
		for plugin in plugins:
			if len(lst) > 0:
				lst += TextFormat.WHITE + ', '

			lst += plugin.isEnable() if TextFormat.GREEN else TextFormat.RED
			lst += plugin.getDescription().getFullName()

		sender.sendMessage(TranslationContainer("pymine.command.plugins.success", [len(plugins), lst]))
