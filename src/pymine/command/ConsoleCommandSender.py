# coding=utf-8
from interface import implements

from pymine.command import CommandSender
from pymine.permission import PermissionAttachment
from pymine.permission.PermissibleBase import PermissibleBase
from pymine.plugin import Plugin


class ConsoleCommandSender(implements(CommandSender)):
    perm = None

    def __init__(self):
        self.perm = PermissibleBase(self)

    def isPermissionSet(self, name):
        return self.perm.isPermissionSet(name)

    def hasPermission(self, name):
        return self.perm.hasPermission(name)

    def addAttachment(self, plugin: Plugin, name=None, value=None):
        return self.perm.addAttachment(plugin, name, value)

    def removeAttachment(self, attachment: PermissionAttachment):
        self.perm.removeAttachment(attachment)
