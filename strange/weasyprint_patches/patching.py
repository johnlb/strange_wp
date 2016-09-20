# coding: utf-8
"""Contain tools related to patching that need to be shared."""


scope = None


def append_scope(func):
	def wrapper(*args,**kwargs):
		return func(args,kwargs)
	return wrapper

