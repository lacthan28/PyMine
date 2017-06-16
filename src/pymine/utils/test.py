# coding=utf-8


class ABCX:
	pass

def getName(abc:ABCX):
	print(type(abc).__name__)

abc = ABCX()
getName(abc)