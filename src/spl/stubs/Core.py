# coding=utf-8
import collections
import datetime
import json
import os
import random

import re

import sys
import urllib.request

import time
import math
import struct


def microtime(get_as_float = False):
	if get_as_float:
		return time.time()
	else:
		return '%f %d' % math.modf(time.time())


def is_numeric(var):
	try:
		float(var)
		return True
	except ValueError:
		return False


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


import types


def function_exists(fun):
	'''As in PHP, fun is tested as a name, not an object as is common in Python.'''
	try:
		ret = type(eval(str(fun)))
		return ret in (types.FunctionType, types.BuiltinFunctionType)
	except NameError:
		return False


def ksort(d):
	return [(k, d[k]) for k in sorted(d.keys())]


def date(unixtime, _format = '%H:%M:%S'):
	d = datetime.datetime.fromtimestamp(unixtime)
	return d.strftime(_format)


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


def array_unshift(array, *args):
	"""Prepend one or more elements to the beginning of an array"""
	for i in reversed(args):
		array.insert(0, i)
	return array


def asort(d):
	return sorted(d.items(), key = lambda x: x[1])


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


class stdClass(object):
	pass


def unpack(fmt, astr):
	"""
	Return struct.unpack(fmt, astr) with the optional single * in fmt replaced with
	the appropriate number, given the length of astr.
	"""
	# http://stackoverflow.com/a/7867892/190597
	try:
		return struct.unpack(fmt, astr)
	except struct.error:
		flen = struct.calcsize(fmt.replace('*', ''))
		alen = len(astr)
		idx = fmt.find('*')
		before_char = fmt[idx - 1]
		n = (alen - flen) / struct.calcsize(before_char) + 1
		fmt = ''.join((fmt[:idx - 1], str(n), before_char, fmt[idx + 1:]))
		return struct.unpack(fmt, astr)
