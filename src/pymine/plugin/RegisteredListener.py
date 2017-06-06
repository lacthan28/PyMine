# coding=utf-8
from pymine.event import Listener, TimingsHandler
from pymine.event.Cancellable import Cancellable
from pymine.event.Event import Event
from pymine.plugin import Plugin, EventExecutor


class RegisteredListener:
    listener = None

    priority = None

    plugin = None

    executor = None

    ignoreCancelled = None

    timings = None

    def __init__(self, listener: Listener, executor: EventExecutor, priority, plugin: Plugin, ignoreCancelled,
                 timings: TimingsHandler):
        self.listener = listener
        self.priority = priority
        self.plugin = plugin
        self.executor = executor
        self.ignoreCancelled = ignoreCancelled
        self.timings = timings

    def getListener(self):
        return self.listener

    def getPlugin(self):
        return self.plugin

    def getPriority(self):
        return self.priority

    def callEvent(self, event: Event):
        if isinstance(event, Cancellable) and event.isCancelled() and self.isIgnoringCancelled():
            return
        self.timings.startTiming()
        self.executor.execute(self.listener, event)
        self.timings.stopTiming()

    def __del__(self):
        self.timings.remove()

    def isIgnoringCancelled(self):
        return self.ignoreCancelled is True
