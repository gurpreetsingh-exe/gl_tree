class Mesh:
	def __init__(self, vertices=None, edges=None, indices=None, uv=None):
		self.vertices = vertices
		self.edges = edges
		self.indices = indices
		self.edges_flat = self.calc_edges()
		self.uv = uv

	def calc_edges(self):
		edges = []
		for edge in self.edges:
			for vert in edge:
				edges.append(self.vertices[vert])

		return edges
