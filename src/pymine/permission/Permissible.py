# coding=utf-8
from zope.interface import Interface

from ..plugin.Plugin import *
from .PermissionAttachment import *
from .ServerOperator import *
from zope.interface import *


class Permissible(Interface):
    implements(ServerOperator)

    def isPermissionSet(self, name): pass

    def hasPermission(self, name): pass

    def addAttachment(self, plugin: Plugin, name=None, value=None): pass

    def removeAttachment(self, attachment: PermissionAttachment): pass

    def recalculatePermissions(self): pass

    def getEffectivePermissions(self): pass
