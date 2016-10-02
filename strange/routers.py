# coding: utf-8
"""
    strange.routers
    ---------------

    A collection of built-in routing tools

"""

class SimpleRouter(object):
	@classmethod
	def route(cls, layout, nets):
		"""Route each net listed in ``nets``

		Returns the ratsnest that remains unrouted.
		"""

		ratsnest = layout[0].netlist
		for net in nets:
			try:
				connections = ratsnest[net]
			except KeyError:
				print("Warning: The net '" + net + 
					"' doesn't exist or has already been routed. ")
				print("         It will be skipped.")
				continue



		return ratsnest