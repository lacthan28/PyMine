from src.pymine.event import Cancellable, HandlerList
class Event:
    eventName = None
    isCancelled = False
    handlerList = None

    def getEventName(self):
        return self.eventName == None if type(self).__name__ else self.eventName

    def isCancelled(self):
        if not isinstance(self, Cancellable):
            raise ValueError("Event is not Cancellable")

        return self.isCancelled() == True

    def setCancelled(self, value = True):
        if not isinstance(self, Cancellable):
            raise ValueError("Event is not Cancellable")

        self.isCancelled = value

    def getHandlers(self):
        if self.handlerList is None:
            self.handlerList = HandlerList()

        return self.handlerLists