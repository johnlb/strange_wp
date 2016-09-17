import numpy as np
import math

PRECISION = 5e-9
UNITS = 1e-6
PPU = UNITS/PRECISION	# Pixels per unit

class geometryContainer():
	"""
	Holds a set of geometries and provides basic manipulations.

	Parameters
	----------
	_geometries : list of translatable gdspy geometry objects.
	"""

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
	
	

	def __init__(self, geometries, extents=None):
		self._geometries = geometries
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
		return 	abs((PPU*(self._extent_right - self._extent_left))), \
				abs((PPU*(self._extent_top - self._extent_bottom)))



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
		delta /= PPU
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
		"""
		Prints all geometries in this container to the gdspy cell given.

		Parameters
		----------
		cell : Cell
			A gdspy cell object

		Modifies
		--------
		cell

		Returns
		-------
		None.

		"""

		[cell.add(geo) for geo in self._geometries]
		return

	
	def _update_extents(self, geometries):
		"""Updates the extents based on a new set of geometries"""
		