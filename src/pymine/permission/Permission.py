# coding=utf-8
from pymine import Server
from pymine.PyMine import is_array
from pymine.isset import isset
from pymine.permission import Permissible

DEFAULT_OP = 'op'
DEFAULT_NOT_OP = 'notop'
DEFAULT_TRUE = 'true'
DEFAULT_FALSE = 'false'


class Permission:
    DEFAULT_PERMISSION = DEFAULT_OP

    @staticmethod
    def getByName(value):
        if isinstance(value, bool):
            if value is True:
                return 'true'
            else:
                return 'false'

        if str.lower(value) is 'op' or 'isop' or 'operator' or 'isoperator' or 'admin' or 'isadmin':
            return DEFAULT_OP
        elif str.lower(value) is '!op' or 'notop' or '!operator' or 'notoperator' or '!admin' or 'notadmin':
            return DEFAULT_NOT_OP
        elif str.lower(value) is 'true':
            return DEFAULT_TRUE
        else:
            return DEFAULT_FALSE

    name = None

    description = None

    children = []

    defaultValue = None

    def __init__(self, name, description=None, defaultValue=None, children: dict = []):
        self.name = name
        self.description = description is not None if description else ''
        self.defaultValue = defaultValue is not None if defaultValue else self.DEFAULT_PERMISSION
        self.children = children

        self.recalculatePermissibles()

    def getName(self):
        return self.name

    def getChildren(self):
        return self.children

    def getDefault(self):
        return self.defaultValue

    def setDefault(self, value):
        if value != self.defaultValue:
            self.defaultValue = value
            self.recalculatePermissibles()

    def getDescription(self):
        return self.description

    def setDescription(self, value):
        self.description = value

    def getPermissibles(self):
        return Server.getInstance().getPluginManager().getPermissionSubscriptions(self.name)

    def recalculatePermissibles(self):
        perms = self.getPermissibles()

        Server.getInstance().getPluginManager().recalculatePermissionDefaults(self)

        for p in perms:
            p.recalculatePermissions()

    def addParent(self, name, value):
        if isinstance(name, Permission):
            name.getChildren()[self.getName()] = value
            name.recalculatePermissibles()
            return None
        else:
            perm = Server.getInstance().getPluginManager().addgetPermission(name)
            if perm is None:
                perm = Permission(name)
                Server.getInstance().getPluginManager().addPermission(perm)

            self.addParent(perm, value)

            return perm

    def loadPermissions(self, data: dict, default=DEFAULT_OP):
        result = []
        for key, entry in data:
            result.append(self.loadPermission(key, entry, default, result))

        return result

    def loadPermission(self, name, data: dict, default=DEFAULT_OP, output=[]):
        desc = None
        children = dict()
        if isset(data['default']):
            value = Permission.getByName(data['default'])
            if value is not None:
                default = value
            else:
                raise ValueError("'default' key contained unknown value")

        if isset(data["children"]):
            if is_array(data["children"]):
                for k, v in data["children"]:
                    if is_array(v):
                        perm = self.loadPermission(k, v, default, output)
                        if perm is not None:
                            output.append(perm)
                    children[k] = True
            else:
                raise ValueError("'children' key is of wrong type")

        if isset(data["description"]):
            desc = data["description"]

        return Permission(name, desc, default, children)
