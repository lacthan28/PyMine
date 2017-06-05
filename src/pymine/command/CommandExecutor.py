from .Command import *
from .CommandSender import *


class CommandExecutor(Interface):
    def onCommand(self, sender: CommandSender, command: Command, label, args: list):
        pass
