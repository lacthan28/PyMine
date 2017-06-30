# -*- coding: utf-8 -*-
from pymine.command.CommandSender import CommandSender
from pymine.command.defaults.VanillaCommand import VanillaCommand
from pymine.event.TranslationContainer import TranslationContainer
from pymine.network.mcpe.protocol.Info import Info
from pymine.plugin.Plugin import Plugin
from pymine.utils.TextFormat import TextFormat


class VersionCommand(VanillaCommand):
	def __init__(self, name):
		VanillaCommand.__init__(self, name,
		                        "%pymine.command.version.description",
		                        "%pymine.command.version.usage",
		                        ['ver', 'about'])

		self.setPermission('pymine.command.version')

	def execute(self, sender: CommandSender, commandLabel, args: dict):
		if not self.testPermission(sender):
			return True

		if len(args) == 0:
			sender.sendMessage(
					TranslationContainer(
							'pymine.server.info.extended',
							[
								sender.getServer().getName(),
								sender.getServer().getPocketMineVersion(),
								sender.getServer().getCodename(),
								sender.getServer().getApiVersion(),
								sender.getServer().getVersion(),
								Info.CURRENT_PROTOCOL
							]
							)
					)
		else:
			pluginName = ' '.join(args)
			exactPlugin = sender.getServer().getPluginManager().getPlugin(pluginName)

			if isinstance(exactPlugin, Plugin):
				self.describeToSender(exactPlugin, sender)
				return True

			found = False
			pluginName = pluginName.lower()
			for plugin in sender.getServer().getPluginManager().getPlugins():
				if plugin.lower().getName().find(pluginName) is not False:
					self.describeToSender(plugin, sender)
					found = True

			if not found:
				sender.sendMessage(TranslationContainer('pymine.command.version.noSuchPlugin'))
		return True

	def describeToSender(self, plugin:Plugin, sender:CommandSender):
		desc = plugin.getDescription()
		sender.sendMessage(TextFormat.DARK_GREEN + desc.getName() + TextFormat.WHITE + ' version ' + TextFormat.DARK_GREEN + desc.getVersion())

		if desc.getDescription() is not None:
			sender.sendMessage(desc.getDescription())

		if desc.getWebsite() is not None:
			sender.sendMessage('Website: ' + desc.getWebsite())

		authors = desc.getAuthors()
		if len(authors) > 0:
			if len(authors) == 1:
				sender.sendMessage('Author: ' + ', '.join(authors))
			else:
				sender.sendMessage('Authors: ' + ', '.join(authors))



