import sudoku_links
import ui
import random
from Node import Node
from Header import Header
from NodeData import NodeData

class DancingLinks(object):
	
	def __init__(self, s=9):
		self.size = s
		self.reset()
		self.listeners = []
		self.canceled = False
	
	def reset(self):
		self.root = sudoku_links.make()
		self.selectedRows = []
		self.solution = []
		self.numSolutions = 0
		self.puzStr = ''
		self.solutionStr = ''
		
	def addToSolution(self, data):
		node = self.findFirst(data)
		self.selectedRows.append(node)
		self.cover(node)
		n = node.right
		while n != node:
			self.cover(n)
			n = n.right
		
	def findFirst(self, data):
		h = self.root.right
		while h != self.root:
			r = h.down
			while r != h:
				if r.data.equals(data):
					return r
				r = r.down
			h = h.right
		return None
		
	def loadPuzzle(self, path):
		puz = ''
		with open(path, 'r') as f:
			lines = [l.strip() for l in f.readlines()]
			self.puzStr = ''.join(lines)
		self.ingestPuzzle(self.puzStr)
		
	def ingestPuzzle(self, puz):
		if len(puz) != 81:
			raise Exception('Invalid Puzzle String; not 81 characters long')
		col = 0
		row = 0
		for c in puz:
			if c not in '0123456789. ':
				raise Exception('Invalid Puzzle String; found bad character: %s' % c)
			if c in '123456789':
				self.addToSolution(NodeData(row, col, int(c) - 1))
			col += 1
			if col >= 9:
				col = 0
				row += 1
		
	def cover(self, node):
		h = self.getHeader(node)
		h.hideLeftRight()
		r = h.down
		while r != h:
			n = r.right
			while n != r:
				n.hideUpDown()
				self.getHeader(n).numRows -= 1
				n = n.right
			r = r.down
		
	def uncover(self, node):
		h = self.getHeader(node)
		r = h.up
		while r != h:
			n = r.left
			while n != r:
				n.unhideUpDown()
				self.getHeader(n).numRows += 1
				n = n.left
			r = r.up
		h.unhideLeftRight()
		
	def solve(self):
		if self.canceled:
			return
		if self.numSolutions > 1:
			return
		if self.root == self.root.right:
			self.solution = self.selectedRows[:]
			self.numSolutions += 1
			sol = self.getSolutionMatrix()
			self.solutionStr = ''.join([''.join([str(r) for r in c]) for c in sol])
			return
		else:
			h = self.getNextCol()
			self.cover(h)
				
			r = h.down
			while r != h:
				self.selectedRows.append(r)
				n = r.right
				while n != r:
					self.cover(n)
					n = n.right
				self.solve()
				self.selectedRows.remove(r)
				n = r.left
				while n != r:
					self.uncover(n)
					n = n.left
				r = r.down
			self.uncover(h)
			
	def getNextCol(self):
		h = self.root.right
		hl = h
		m = h.numRows
		while h != self.root:
			if h.numRows < m:
				hl = h
				m = h.numRows
			h = h.right
		return hl
		
	def getRandomCol(self):
		h = self.root
		for x in range (random.randint(1, 9**2 * 4)):
			h = h.right
		if h == self.root:
			h = h.right
		return h
				
	def getSolutionMatrix(self):
		g = [[0 for x in range(self.size)] for x in range(self.size)]
		for n in self.solution:
			d = n.data
			g[d.r][d.c] = d.n + 1
		return g
		
	def getHeader(self, node):
		curNode = node
		while not isinstance(curNode, Header):
			curNode = curNode.up
		return curNode
		
	def registerListener(self, listener):
		self.listeners.append(listener)
		
	def start(self):
		self.solve()
		for l in self.listeners:
			l.finished()
		
	def cancel(self):
		self.canceled = True
