# coding=utf-8
from spl.stubs.isset import isset
from .Permissible import *
from .ServerOperator import *


class PermissibleBase:
    implements(Permissible)
    opable = None

    parent = None

    attachments = []

    permissions = []

    def __init__(self, opable: ServerOperator):
        self.opable = opable
        if isinstance(opable, Permissible):
            self.parent = opable

    def __del__(self):
        self.parent = None
        self.opable = None

    def isOp(self):
        if self.opable is None:
            return False
        else:
            return self.opable.isOp()

    def setOp(self, value):
        if self.opable is None:
            raise ValueError("Cannot change op value as no ServerOperator is set")
        else:
            self.opable.setOp(value)

    def isPermissionSet(self, name):
        return isset(self.permissions[isinstance(name, Permission)])

    def hasPermission(self, name):
        pass

    def addAttachment(self, plugin, name, value):
        pass

    def removeAttachment(self, attachment):
        pass

    def recalculatePermissions(self):
        pass

    def clearPermissions(self):
        pass

    def calculateChildPermissions(self, children: list, invert, attachment):
        pass
