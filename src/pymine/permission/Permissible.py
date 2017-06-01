from ..plugin.Plugin import *
from .PermissionAttachment import *
from .ServerOperator import *


class Permissible(ServerOperator):
    def isPermissionSet(self, name): pass

    def hasPermission(self, name): pass

    def addAttachment(self, plugin: Plugin, name=None, value=None): pass

    def removeAttachment(self, attachment: PermissionAttachment): pass

    def recalculatePermissions(self): pass

    def getEffectivePermissions(self): pass
