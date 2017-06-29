# -*- coding: utf-8 -*-
import os
from abc import ABCMeta
from getopt import getopt

import sys

from pymine.utils.Utils import Utils
from spl.stubs.Core import isset, function_exists


class Terminal(metaclass = ABCMeta):
	FORMAT_BOLD = ""
	FORMAT_OBFUSCATED = ""
	FORMAT_ITALIC = ""
	FORMAT_UNDERLINE = ""
	FORMAT_STRIKETHROUGH = ""

	FORMAT_RESET = ""

	COLOR_BLACK = ""
	COLOR_DARK_BLUE = ""
	COLOR_DARK_GREEN = ""
	COLOR_DARK_AQUA = ""
	COLOR_DARK_RED = ""
	COLOR_PURPLE = ""
	COLOR_GOLD = ""
	COLOR_GRAY = ""
	COLOR_DARK_GRAY = ""
	COLOR_BLUE = ""
	COLOR_GREEN = ""
	COLOR_AQUA = ""
	COLOR_RED = ""
	COLOR_LIGHT_PURPLE = ""
	COLOR_YELLOW = ""
	COLOR_WHITE = ""

	formattingCodes = None

	@staticmethod
	def hasFormattingCodes():
		if Terminal.formattingCodes is None:
			opts = getopt(sys.argv, "", ["enable-ansi", "disable-ansi"])
			if isset(opts["disable-ansi"]):
				Terminal.formattingCodes = False
			else:
				Terminal.formattingCodes = Utils.getOS() != 'win' and os.environ["TERM"] != "" and not function_exists("posix_ttyname") or "STDOUT".
