"""Searches for and imports a specified tech module as 'tech'"""

import imp


tech = None

__all__ = ['tech']


def init_techfile(tech_name, extra_dirs=[]):
	global tech
	TECH_DIR = ['../techlibs/'].append(extra_dirs)
	try:
		found = imp.find_module(tech_name, [TECH_DIR])
		tech = imp.load_module(tech_name,*found)
	except ImportError as e:
		raise Exception('Technology files for "' + e.name + '" not found.')


