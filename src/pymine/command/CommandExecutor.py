from .Command import *
from .CommandSender import *
from array import *


class CommandExecutor:
    def onCommand(self, sender: CommandSender, command: Command, label, args:array):
        pass
