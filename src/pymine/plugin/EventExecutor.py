# coding=utf-8
from zope.interface import Interface

from pymine.event import Listener, Event


class EventExecutor(Interface):
    def execute(self, listener: Listener, event: Event): pass
