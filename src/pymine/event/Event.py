# coding=utf-8
from .Cancellable import *
from .HandlerList import *
from abc import *


class Event(metaclass=ABCMeta):
    eventName = None
    varIsCancelled = False

    def getEventName(self):
        return self.eventName is None if type(self).__name__ else self.eventName

    def isCancelled(self):
        if not isinstance(self, Cancellable):
            raise BaseException("Event is not Cancellable")

        return Event.varIsCancelled is True

    def setCancelled(self, value=True):
        if not isinstance(self, Cancellable):
            raise BaseException("Event is not Cancellable")

        Event.varIsCancelled = bool(value)

    def getHandlers(self):
        global handlerList
        if handlerList is None:
            handlerList = HandlerList()

        return handlerList
