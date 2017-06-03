from .standard.basic import __FILE__, __LINE__
from typing import *


class stdClass:
    pass


class iterable:
    pass


class Traversable(iterable):
    pass


class IteratorAggregate(Traversable):
    def getIterator(self): pass


class Iterator(Traversable):
    def current(self): pass

    def next(self): pass

    def key(self): pass

    def valid(self): pass

    def rewind(self): pass


class ArrayAccess:
    class ArrayAccess(object):
        def __getitem__(self, key):
            return self.container

    def __setitem__(self, key, value):
        self.container = value

    def __delitem__(self, key, value):
        del self.container


class Serializable:
    def serializable(self): pass

    def unserializable(self, serializabled): pass


class Throwable:
    def getMessage(self): pass

    def getCode(self): pass

    def getFile(self): pass

    def getLine(self): pass

    def getTrace(self): pass

    def getTraceAsString(self): pass

    def getPrevious(self): pass

    def __toString(self): pass


class Exception(Throwable):
    message, code, file, line = None

    def __clone(self): pass

    def __init__(self, message="", code=0, previous: Throwable = None): pass

    def getMessage(self): pass

    def getCode(self): pass

    def getFile(self): pass

    def getLine(self): pass

    def getTrace(self): pass

    def getPrevious(self): pass

    def getTraceAsString(self): pass

    def __toString(self): pass


class Error(Throwable):
    def __init__(self, message="", code=0, previous: Throwable = None): pass

    def getMessage(self): pass

    def getCode(self): pass

    def getFile(self): pass

    def getLine(self): pass

    def getTrace(self): pass

    def getPrevious(self): pass

    def getTraceAsString(self): pass

    def __toString(self): pass


class TypeError(Error): pass


class ParseError(Error): pass


class AssertionError(Error): pass


class ArithmeticError(Error): pass


class DivisionByZeroError(Error): pass


class ErrorException(Exception):
    severity = None

    def __init__(self, message="", code=0, severity=1, filename=__FILE__, lineno=__LINE__, previous=None): pass

    def getSeverity(self): pass


class Closure:
    def __init__(self): pass

    def __invoke(self, _): pass

    def bindTo(self, newthis, newscope='static'): pass

    def bind(self, Closure, newthis, newscope='static'): pass

    def call(self, newThis, parameters): pass

    def fromCallable(self, callable: Callable): pass
