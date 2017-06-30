# -*- coding: utf-8 -*-
import sys

from pymine.command.Command import Command
from pymine.command.CommandSender import CommandSender
from pymine.command.ConsoleCommandSender import ConsoleCommandSender
from pymine.command.data.CommandParameter import CommandParameter
from pymine.command.defaults.VanillaCommand import VanillaCommand
from pymine.event.TranslationContainer import TranslationContainer
from pymine.utils.TextFormat import TextFormat
from spl.stubs.Core import ksort, isset


class HelpCommand(VanillaCommand):
	def __init__(self, name):
		VanillaCommand.__init__(
				self,
				name,
				"%pymine.command.help.description",
				"%commands.help.usage")
		self.setPermission('pymine.command.help')
		self.commandParameters['default'] = [CommandParameter('page', CommandParameter.ARG_TYPE_INT, False)]

	def execute(self, sender: CommandSender, currentAlias, args: dict):
		if not self.testPermission(sender):
			return True

		if len(args) == 0:
			command = ''
			pageNumber = 1
		elif args[len(args) - 1].isnumeric():
			pageNumber = int(args.pop())
			if pageNumber <= 0:
				pageNumber = 1
			command = ' '.join(args)
		else:
			command = ' '.join(args)
			pageNumber = 1

		if isinstance(sender, ConsoleCommandSender):
			pageHeight = sys.int_info.__getattribute__('sizeof_digit')
		else:
			pageHeight = 7

		if command == '':
			commands = []
			for command in sender.getServer().getCommandMap().getCommands:
				if command.testPermissionSilent(sender):
					commands[command.getName()] = command

			ksort(commands)
			commands = [commands[i: i + pageHeight] for i in range(0, len(commands), pageHeight)]
			pageNumber = int(min(len(commands), pageNumber))
			if pageNumber < 1:
				pageNumber = 1

			sender.sendMessage(TranslationContainer("commands.help.header", [pageNumber, len(commands)]))

			if isset(commands[pageNumber]):
				for command in commands[pageNumber - 1]:
					sender.sendMessage(
						TextFormat.DARK_GREEN + "/" + command.getName() + ": " + TextFormat.WHITE + command.getDescription())

			return True
		else:
			cmd = sender.getServer().getCommandMap().getCommand(command.lower())
			if isinstance(cmd, Command):
				if cmd.testPermissionSilent(sender):
					message = TextFormat.YELLOW + "--------- " + TextFormat.WHITE + " Help: /" + cmd.getName() + TextFormat.YELLOW + " ---------\n"
					message += TextFormat.GOLD + "Description: " + TextFormat.WHITE + cmd.getDescription() + "\n"
					message += TextFormat.GOLD + "Usage: " + TextFormat.WHITE + ("\n" + TextFormat.WHITE).join(
						cmd.getUsage().split('\n')) + "\n"
					sender.sendMessage(message)

					return True

			sender.sendMessage(TextFormat.RED + "No help for " + command.lower())
			return True
