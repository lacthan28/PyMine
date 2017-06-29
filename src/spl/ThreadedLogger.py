# -*- coding: utf-8 -*-
from threading import Thread
from abc import ABCMeta
from logging import Logger


class ThreadedLogger(metaclass = ABCMeta, Logger, Thread):
	pass
