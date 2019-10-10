from NodeData import NodeData

class Node (object):
	
	def __init__(self, r=-1, c=-1, n=-1):
		self.data = NodeData(r,c,n)
		self.left = self
		self.right = self
		self.up = self
		self.down = self
		
	def hideLeftRight(self):
		self.right.left = self.left
		self.left.right = self.right
	def unhideLeftRight(self):
		self.right.left = self
		self.left.right = self
	def hideUpDown(self):
		self.up.down = self.down
		self.down.up = self.up
	def unhideUpDown(self):
		self.up.down = self
		self.down.up = self
		
	def addRight(self, o):
		o.left = self
		o.right = self.right
		self.right.left = o
		self.right = o
	def addLeft(self, o):
		o.right = self
		o.left = self.left
		self.left.right = o
		self.left = o
	def addUp(self, o):
		o.down = self
		o.up = self.up
		self.up.down = o
		self.up = o
	def addDown(self, o):
		o.up = self
		o.down = self.down
		self.down.up = o
		self.down = o
		
	def __repr__(self):
		return str(self.data)
