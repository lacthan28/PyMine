# coding=utf-8
from .Server import *
import os


class OfflinePlayer:
    name = None
    server = None
    namedtag = None

    """
    @:param server: Server
    @:param name: String
    """

    def __init__(self, server: Server, name):
        self.server = server
        self.name = name
        if os.path.exists(self.server.getDataPath() + "players/" + str.lower(self.getName()) + ".dat"):
            self.namedtag = self.server.getOfflinePlayerData(self.name)
        else:
            self.namedtag = None

    def getName(self):
        return self.name
