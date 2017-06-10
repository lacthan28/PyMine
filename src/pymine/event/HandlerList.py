# coding=utf-8
from pymine.plugin.RegisteredListener import *
from spl.stubs.isset import *
from .EventPriority import *
from .Listener import *
from .plugin.Plugin import *


class HandlerList:
    handlers = None

    handlerSlots = []

    allLists = []

    def bakeAll(self):
        for h in self.allLists:
            h.bake()

    def unregisterAll(self, object=None):
        if isinstance(object, Listener) or isinstance(object, Plugin):
            for h in self.allLists:
                h.unregister(object)
        else:
            for h in self.allLists:
                for key, list in h.handlerSlots:
                    h.handlerSlots[key] = []
                h.handlers = None

    def __init__(self):
        self.handlerSlots = {
            EventPriority.LOWEST: [],
            EventPriority.LOW: [],
            EventPriority.NORMAL: [],
            EventPriority.HIGH: [],
            EventPriority.HIGHEST: [],
            EventPriority.MONITOR: []
        }
        self.allLists.append(self)

    def register(self, listener: RegisteredListener):
        if listener.getPriority() < EventPriority.MONITOR or listener.getPriority() > EventPriority.LOWEST:
            return
        if isset(self.handlerSlots[listener.getPriority()][listener.__hash__()]):
            raise BaseException("This listener is already registered to priority " + listener.getPriority())
        self.handlers = None
        self.handlerSlots[listener.getPriority()][listener.__hash__()] = listener

    def registerAll(self, listeners: list):
        for listener in listeners:
            self.register(listener)

    def unregister(self, object):
        if isinstance(object, Listener) or isinstance(object, Plugin):
            changed = False
            for priority, list in self.handlerSlots:
                for hash, listener in list:
                    if (isinstance(object, Plugin) and listener.getPlugin() is object) or (
                                isinstance(object, Listener) and listener.getListener() is object):
                        del self.handlerSlots[priority][hash]
                        changed = True
            if changed is True:
                self.handlers = None
        elif isinstance(object, RegisteredListener):
            if isset(self.handlerSlots[object.getPriority()][object.__hash__()]):
                del self.handlerSlots[object.getPriority()][object.__hash__()]
                self.handlers = None

    def bake(self):
        if self.handlers is not None:
            return
        entries = []
        for list in self.handlerSlots:
            for hash, listener in list:
                entries[hash] = listener
        self.handlers = entries

    def getRegisteredListeners(self, plugin=None):
        if plugin is not None:
            listeners = []
            for hash, listener in self.getRegisteredListeners(None):
                if listener.getPlugin() is plugin:
                    listeners[hash] = plugin

            return listeners
        else:
            while self.handlers is None:
                self.bake()
            return self.handlers

    def getHandlerLists(self):
        return self.allLists
