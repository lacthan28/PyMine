# coding=utf-8
import logging

try:
	print(1/0)
except BaseException as e:
	print(logging.exception(e))
