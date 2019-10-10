class NodeData (object):
	def __init__(self, r=-1, c=-1, n=-1):
		self.set(r,c,n)
	def set(self, r=-1, c=-1, n=-1):
		self.r = r
		self.c = c
		self.n = n
	def equals(self, o):
		return self.r == o.r and self.c == o.c and self.n == o.n
	def __repr__(self):
		return '[%s,%s]:%s' % (self.c, self.r, self.n)
