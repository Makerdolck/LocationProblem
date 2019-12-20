class Cell(object):
	"""description of class"""
	def __init__(self, type='way', x = 0, y = 0):
		self.type = type
		self.x = x
		self.y = y
		self.weight = 0
		#self.previous = self