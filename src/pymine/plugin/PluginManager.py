# -*- coding: utf-8 -*-
from collections import Mapping

from pymine.Server import Server
from pymine.command.SimpleCommandMap import SimpleCommandMap
from pymine.permission.Permission import Permission
from pymine.plugin.Plugin import Plugin


class PluginManager:
	server = Server
	commandMap=SimpleCommandMap
	plugins = [Plugin() for plugin in range(100)]
	permissions = [Permission() for permission in range(100)]
