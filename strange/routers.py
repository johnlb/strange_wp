# coding: utf-8
"""
    strange.routers
    ---------------

    A collection of built-in routing tools

"""

import gdspy


class SimpleRouter(object):
	@classmethod
	def route(cls, layout, nets):
		"""Route each net listed in ``nets``

		Returns the ratsnest that remains unrouted.
		"""

		ratsnest = layout.netlist
		for net in nets:
			try:
				net_geometries = ratsnest[net]
			except KeyError:
				print("Warning: The net '" + net + 
					"' doesn't exist or has already been routed. ")
				print("         It will be skipped.")
				continue

			cls.auto_via_fill(layout, net_geometries)


		return ratsnest


	@classmethod
	def auto_via_fill(cls, layout, geometries):
		"""Automatically connect any overlapping layers with vias.
		"""
		tech = layout.tech

		# ugeos = cls._get_geometries_on_layer(geometries, tech.routing_layers[0])
		# for ii, llayer in enumerate(tech.routing_layers[1:-2]):
		# 	ulayer = tech.routing_layers[ii+1]
		# 	vlayer = tech.via_layers[ii]

		for llayer, ulayer in tech.stackup.via_layers:
			lgeos = cls._get_geometries_on_layer(geometries, llayer)
			ugeos = cls._get_geometries_on_layer(geometries, ulayer)
			vlayer = tech.via_layers[(llayer, ulayer)]
			if (ugeos==[]) or (lgeos==[]):
				continue

			overlap = cls._find_overlap(lgeos,ugeos)
		
			[layout.add(x) for x in tech.Vias.draw_vias( overlap,
														 vlayer )]
			


	@classmethod
	def _find_overlap(cls, geos1, geos2, layer=0):
		"""Return a geometry on layer 0 that represents any overlap
		in geometries.
		"""
		geos1 = cls._union_of_geometries(geos1, layer)
		geos2 = cls._union_of_geometries(geos2, layer)
		return gdspy.fast_boolean(geos1,geos2,'and',layer=layer)


	@classmethod
	def _get_geometries_on_layer(cls, geometries, layer):
		"""Return all objects in ``geometries`` that exist on ``layer``"""
		result = []
		for geo in geometries:
			if geo.layer==layer:
				result.append(geo)
		return result


	@classmethod
	def _union_of_geometries(cls, geometries, layer):
		"""Returns union of all geometries in list ``geometries``"""
		result = geometries[0]
		for geo in geometries[1:]:
			result = gdspy.fast_boolean(result, geo, 'or', layer=layer)

		return result