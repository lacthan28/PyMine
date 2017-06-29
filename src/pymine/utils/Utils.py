# -*- coding: utf-8 -*-
from spl.stubs.Core import is_array
import hashlib, platform, os


class Utils:
	online = True
	ip = False
	os = None
	serverUniqueId = None

	@staticmethod
	def getCallableIdentifier(func):
		if is_array(func):
			return hashlib.sha1(str.lower(str(hash(func[0])))) + "." + str.lower(func[1])
		else:
			return hashlib.sha1(str.lower(func))

	@staticmethod
	def getMachineUniqueId(extra = ""):
		if Utils.serverUniqueId is not None and extra == "":
			return Utils.serverUniqueId

	@staticmethod
	def getOS(recalculate = False):
		if Utils.os is None or recalculate:
			uname = platform.system() + " " + os.name.upper()
			if str.upper(uname).find(str.upper("Darwin")) is not False:
				if "iP" in platform.uname().__getattribute__("machine") == 0:
					Utils.os = "ios"
				else:
					Utils.os = "mac"
			elif str.upper(uname).find(str.upper("Win")) is not False or uname == "Msys":
				Utils.os = "win"
			elif str.upper(uname).find(str.upper("Linux")) is not False:
				try:
					if os.path.exists("/system/build.prop"):
						Utils.os = "android"
					else:
						Utils.os = "linux"
				except FileExistsError as e:
					raise e
			elif str.upper(uname).find(str.upper("BSD")) is not False or uname == "DragonFly":
				Utils.os = "bsd"
			else:
				Utils.os = "other"
		return Utils.os

	@staticmethod
	def getRealMemoryUsage():
		stack = 0
		heap = 0

		if Utils.getOS() == "linux" or Utils.getOS() == "android":
			mappings = open("/proc/self/maps").readlines()
			for line in mappings:
				pass
			# TODO: undone
