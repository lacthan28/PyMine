# -*- coding: utf-8 -*-
from pymine.Server import Server
from pymine.command.Command import Command
from pymine.command.CommandMap import CommandMap
from pymine.command.defaults.HelpCommand import HelpCommand
from pymine.command.defaults.PluginsCommand import PluginsCommand
from pymine.command.defaults.SeedCommand import SeedCommand
from pymine.command.defaults.VersionCommand import VersionCommand


class SimpleCommandMap(CommandMap):
	_knownCommands = dict(Command)

	__server = Server

	def __init__(self, server:Server):
		self.__server = server
		self.setDefaultCommands()

	def setDefaultCommands(self):
		self.register("pocketmine", VersionCommand("version"))
		self.register("pocketmine", PluginsCommand("plugins"))
		self.register("pocketmine", SeedCommand("seed"))
		self.register("pocketmine", HelpCommand("help"))
		self.register("pocketmine", StopCommand("stop"))
		self.register("pocketmine", TellCommand("tell"))
		self.register("pocketmine", DefaultGamemodeCommand("defaultgamemode"))
		self.register("pocketmine", BanCommand("ban"))
		self.register("pocketmine", BanIpCommand("ban-ip"))
		self.register("pocketmine", BanListCommand("banlist"))
		self.register("pocketmine", PardonCommand("pardon"))
		self.register("pocketmine", PardonIpCommand("pardon-ip"))
		self.register("pocketmine", SayCommand("say"))
		self.register("pocketmine", MeCommand("me"))
		self.register("pocketmine", ListCommand("list"))
		self.register("pocketmine", DifficultyCommand("difficulty"))
		self.register("pocketmine", KickCommand("kick"))
		self.register("pocketmine", OpCommand("op"))
		self.register("pocketmine", DeopCommand("deop"))
		self.register("pocketmine", WhitelistCommand("whitelist"))
		self.register("pocketmine", SaveOnCommand("save-on"))
		self.register("pocketmine", SaveOffCommand("save-off"))
		self.register("pocketmine", SaveCommand("save-all"))
		self.register("pocketmine", GiveCommand("give"))
		self.register("pocketmine", EffectCommand("effect"))
		self.register("pocketmine", EnchantCommand("enchant"))
		self.register("pocketmine", ParticleCommand("particle"))
		self.register("pocketmine", GamemodeCommand("gamemode"))
		self.register("pocketmine", KillCommand("kill"))
		self.register("pocketmine", SpawnpointCommand("spawnpoint"))
		self.register("pocketmine", SetWorldSpawnCommand("setworldspawn"))
		self.register("pocketmine", TeleportCommand("tp"))
		self.register("pocketmine", TimeCommand("time"))
		self.register("pocketmine", TimingsCommand("timings"))
		self.register("pocketmine", TitleCommand("title"))
		self.register("pocketmine", ReloadCommand("reload"))
		self.register("pocketmine", WeatherCommand("weather"))
		self.register("pocketmine", TransferCommand("transfer"))
		self.register("pocketmine", XpCommand("xp"))