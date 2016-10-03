import numpy as np
import math



class GenericContainer(object):
	"""Base-class for all geometry containers. Not meant to be used directly"""

	@property
	def netlist(self):
		return self._netlist

	@netlist.setter
	def netlist(self, netlist):
		self._netlist = netlist


	def __init__(self, geometries=[], netlist={}, tech=None):
		self.tech 	= tech
		self.PPU	= self.tech.units / self.tech.precision

		self._geometries = geometries
		self._netlist = netlist


	def add(self, geometry):
		self._geometries.append(geometry)








class CellContainer(GenericContainer):
	"""Holds both bare geometries and DeviceContainers. For complete layouts"""

	def __init__(self, geometries=[], netlist={}, tech=None):
		super().__init__(geometries, netlist, tech)
		self._devices 	= []
		self._by_layer 	= {}


	def add(self, obj, net=''):
		if isinstance(obj, DeviceContainer):
			self._devices.append(obj)
			# add device's interface to overall netlist
			interface = obj.netlist
			for pin in interface.values():
				net 		= pin[0]
				geometries  = pin[1]
				[self._add_to_netlist(net, geo) for geo in geometries]

		else:
			self._geometries.append(obj)
			self._add_to_netlist(net, obj)


	def _add_to_netlist(self, net, geo):
		if net=='':
			return

		try:
			self._netlist[net].append(geo)
		except KeyError:
			self._netlist[net] = [geo]

		try:
			self._by_layer[geo.layer].append(geo)
		except KeyError:
			self._by_layer[geo.layer] = [geo]


	def draw(self, context):
		for geo in self._geometries:
			context.add(geo)
		for dev in self._devices:
			dev.draw(context)


	def get_geometries_on_layer(self, layer):
		"""Return a list of all geometries on ``layer``"""
		try:
			return self._by_layer[layer]
		except KeyError:
			return []





class DeviceContainer(GenericContainer):
	"""Holds a set of geometries and provides basic manipulations."""


	
	@property
	def extent_left(self):
	    return self._extent_left

	@property
	def extent_right(self):
	    return self._extent_right

	@property
	def extent_top(self):
	    return self._extent_top
	
	@property
	def extent_bottom(self):
	    return self._extent_bottom

	@property
	def intrinsic_ratio(self):
		width, height = self.get_intrinsic_size('','')
		self._intrinsic_ratio = width/height
		return self._intrinsic_ratio
	
	

	def __init__(self, geometries, netlist, tech, extents=None):

		super().__init__(geometries, netlist, tech)
		self._update_extents(geometries)

		try:
			self._extent_top    = extents[0]
			self._extent_right  = extents[1]
			self._extent_bottom = extents[2]
			self._extent_left   = extents[3]
		except TypeError:
			# Figure it out your self...
# TODO: add code to figure out extents
			self._extent_top    = None
			self._extent_right  = None
			self._extent_bottom = None
			self._extent_left   = None


	def get_intrinsic_size(self, dont, need):
		"""Returns the width and height of all geometries."""
		return 	abs((self.PPU*(self._extent_right - self._extent_left))), \
				abs((self.PPU*(self._extent_top - self._extent_bottom)))



	def translate(self, delta):
		"""
		Moves all objects by delta := [dx, dy]
		(delta measured in units)

		Parameters
		----------
		delta : [dx, dy]
			List of two floats.
			dx: distance to move in x-direction
			dy: distance to move in y-direction

		Returns
		-------
		self : geometryContainer
		"""
		delta = np.array(delta,dtype='float')
		for geo in self._geometries:
			geo.translate(delta[0], delta[1])

		self._extent_left   += delta[0]
		self._extent_right  += delta[0]
		self._extent_top    += delta[1]
		self._extent_bottom += delta[1]

		return self


	def translate_px(self, delta):
		"""
		Moves all objects by delta := [dx, dy]
		(delta measured in pixels)

		Parameters
		----------
		delta : [dx, dy]
			List of two floats.
			dx: distance to move in x-direction
			dy: distance to move in y-direction

		Returns
		-------
		self : geometryContainer
		"""
		delta = np.array(delta,dtype='float')
		delta /= self.PPU
		for geo in self._geometries:
			geo.translate(delta[0], delta[1])

		self._extent_left   += delta[0]
		self._extent_right  += delta[0]
		self._extent_top    += delta[1]
		self._extent_bottom += delta[1]

		return self

	def rotate(self, angle):
		"""
		TO DO
		"""

	def flip(self, axis):
		"""
		TO DO
		"""

	def draw(self, cell):
		"""Prints all geometries in this container to the gdspy cell given."""

		[cell.add(geo) for geo in self._geometries]


	
	def _update_extents(self, geometries):
		"""Updates the extents based on a new set of geometries"""
		# TODO: finish this.
		pass


