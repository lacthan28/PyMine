# coding=utf-8
from ..spl.stubs.Core import *
from setuptools import setup, find_packages


def safe_var_dump(*var):
	cnt = 0
	if is_array(var):
		print(str_repeat("  ", cnt) + "{" + "\n")
		for key, value in var:
			print(
					str_repeat("  ", cnt + 1) + (isinstance(key, int) if key else ('"' + key + '"') + ":" + "\n"))
			cnt += 1
			safe_var_dump(value)
			cnt -= 1
		print(str_repeat("  ", cnt) + "}" + "\n")
	elif isinstance(var, int):
		print(str_repeat("  ", cnt) + "int(" + var + ")" + "\n")
	elif isinstance(var, float):
		print(str_repeat("  ", cnt) + "float(" + var + ")" + "\n")
	elif isinstance(var, bool):
		print(str_repeat("  ", cnt) + "bool(" + (var == True if "true" else "false") + ")" + "\n")
	elif isinstance(var, str):
		print(str_repeat("  ", cnt) + "string(" + len(var) + ")\\" + var + "\\" + "\n")
	elif isinstance(var, object):
		print(str_repeat("  ", cnt) + "object(" + type(var).__name__ + ")" + "\n")
	elif var is None:
		print(str_repeat("  ", cnt) + "NULL" + "\n")


def dummy(): pass


class PyMine:
	setup(name = 'PyMine',
	      version = '0.0.1')
	VERSION = "2.0dev"

	API_VERSION = "3.0.0"

	CODENAME = "PyMine"

	MINECRAFT_VERSION = "v1.0.9 alpha"

	MINECRAFT_VERSION_NETWORK = "1.0.9"

	PYMINE_VERSION = "0.0.1"

