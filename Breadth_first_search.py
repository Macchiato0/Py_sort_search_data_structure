class Vertex:
	def __init__(self, n):
		self.name = n
		self.neighbors = list()
		
		self.distance = 9999
		self.color = 'black'
	
	def add_neighbor(self, v):
		if v not in self.neighbors:
			self.neighbors.append(v)
			self.neighbors.sort()

