# -*- coding: utf-8 -*-
import os

from pymine.utils.MainLogger import MainLogger
from spl.stubs.Core import substr, isset


class BaseLang:
	FALLBACK_LANGUAGE = "eng"

	@staticmethod
	def getLanguageList(path: str = "") -> dict:
		if path == "":
			path = os.path.dirname(os.path.realpath(__file__)) + "\\locale\\"

		if os.path.isdir(path):
			allFiles = os.listdir(path)

			if allFiles is not False:
				files = filter(lambda filename: substr(filename, -4) == ".ini", allFiles)

				result = { }

				for file in files:
					strings = { }
					BaseLang.loadLang(path + file, strings)
					if isset(strings['language.name']):
						result[substr(file, 0, -4)] = strings['language.name']
				return result
		return { }

	langName=None

	lang ={}
	fallbackLang={}

	def __init__(self, lang:str, path=None, fallback = FALLBACK_LANGUAGE):
		self.langName = lang.lower()

		if path is None:
			path = os.path.dirname(os.path.realpath(__file__)) + "\\locale\\"

		file = path + self.langName + ".ini"
		if not BaseLang.loadLang(file,self.lang):
			MainLogger.getLogger().error("Missing required language file {}".format(file))
