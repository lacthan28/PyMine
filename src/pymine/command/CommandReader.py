# -*- coding: utf-8 -*-
import sys, getopt
from threading import Thread


class CommandReader(Thread):
	TYPE_READLINE = 0
	TYPE_STREAM = 1
	TYPE_PIPED = 2

	buffer = None
	shutdown = False
	_type = TYPE_STREAM

	def __init__(self):
		self.buffer = Thread()
		opts = getopt(sys.argv, "", ["disable-readline"])