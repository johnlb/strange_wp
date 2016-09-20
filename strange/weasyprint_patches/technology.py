# coding: utf-8
"""Searches for and imports a specified tech module as 'tech'"""

import imp
import sys


tech = None

__all__ = ['tech']


def init_techfile(tech_name, extra_dirs=[]):
	global tech
	DEFAULT_DIR = ['/home/johnlb/opensource/strange_wp/techlibs/']
	TECH_DIR = DEFAULT_DIR + extra_dirs
	try:
		found = imp.find_module(tech_name, TECH_DIR)
		tech = imp.load_module(tech_name,*found)
	except ImportError as e:
		raise Exception('Technology files for "' + e.name + '" not found.')


