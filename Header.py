from Node import Node

class Header (Node):
	def __init__(self, r=-1, c=-1, n=-1):
		Node.__init__(self,r,c,n)
		self.numRows = 0
