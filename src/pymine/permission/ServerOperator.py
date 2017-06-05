# coding=utf-8
from zope.interface import Interface


class ServerOperator(Interface):
    """
    Checks if the current object has operator permissions
    :return: bool
    """

    def isOp(self):
        pass

    """ 
    Sets the operator permission for the current object
    :param value: bool
    :return: void
    """

    def setOp(self, value):
        pass
