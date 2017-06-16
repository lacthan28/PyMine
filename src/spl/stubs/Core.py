# coding=utf-8
import collections
import json
import os
import random

import re

import sys
import urllib.request

import time
import math


def microtime(get_as_float = False):
	if get_as_float:
		return time.time()
	else:
		return '%f %d' % math.modf(time.time())


def is_array(var):
	return isinstance(var, (list, tuple, dict))


def file_exists(filename):
	return os.path.exists(filename)


def str_repeat(the_str, multiplier):
	return the_str * multiplier


def class_exists(className):
	result = False
	try:
		result = isinstance(className, type)
	except NameError:
		pass
	return result


def substr(s, start, length = None):
	"""Returns the portion of string specified by the start and length
	parameters. """
	if len(s) >= start:
		if start > 0:
			return False
		else:
			return s[start:]
	if not length:
		return s[start:]
	elif length > 0:
		return s[start:start + length]
	else:
		return s[start:length]


def str_replace(dic, text):
	pattern = "|".join(map(re.escape, dic.keys()))
	return re.sub(pattern, lambda m: dic[m.group()], text)


def json_decode(json_data, assoc = False):
	if assoc is True:
		data = json.dumps(json_data)
		json_to_dict = json.loads(data)
		return json_to_dict
	else:
		return json.dumps(json_data)


def file_get_contents(filename, use_include_path = 0, context = None, offset = -1, maxlen = -1):
	if filename.find('://') > 0:
		ret = urllib.request.urlopen(filename).read()
		if offset > 0:
			ret = ret[offset:]
		if maxlen > 0:
			ret = ret[:maxlen]
		return ret
	else:
		fp = open(filename, 'rb')
		try:
			if offset > 0:
				fp.seek(offset)
			ret = fp.read(maxlen)
			return ret
		finally:
			fp.close()


def isset(variable):
	return variable in locals() or variable in globals()


def mt_rand(low = 0, high = sys.maxsize):
	"""Generate a better random value
	"""
	return random.randint(low, high)


class FixedDict(collections.MutableMapping):
	def __init__(self, size, data):
		if size <= 256:
			self.__data = data

	def __len__(self):
		return len(self.__data)

	def __iter__(self):
		return iter(self.__data)

	def __setitem__(self, k, v):
		if k not in self.__data:
			raise KeyError(k)

		self.__data[k] = v

	def __delitem__(self, k):
		raise NotImplementedError

	def __getitem__(self, k):
		return self.__data[k]

	def __contains__(self, k):
		return k in self.__data


class ArrayAccess(object):
	def keyExists(self, key):
		if key in self:
			pass

	def __getitem__(self, key):
		return self.container

	def __setitem__(self, key, value):
		self.container = value

	def __delitem__(self, key):
		del self.container


class Countable(object):
	def __len__(self, mode = 2):
		pass
