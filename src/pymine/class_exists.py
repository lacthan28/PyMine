# coding=utf-8
import types


def class_exists(className):
    result = False
    try:
        result = isinstance(className, type)
    except NameError:
        pass
    return result
