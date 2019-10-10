import ui
from wrapper import WrapInstance

class SudokuGrid (ui.View):
	
	def __init__(self):
		v = ui.load_view('/'.join(__name__.split('.')),bindings={self.__class__.__name__:WrapInstance(self),'self':self})
		self.txtGrid = [[None for x in range(9)] for x in range(9)]
		for c in range(9):
			for r in range(9):
				self.txtGrid[c][r] = v['cell%s%s' % (c,r)]
				self.initTxtField(self.txtGrid[c][r],r,c)
		self.resetGrid(True)
				
	def resetGrid(self, first=False):
		if not first:
			for c in range(9):
				for r in range(9):
					self.txtGrid[c][r].text = ''
		self.givens = []
		self.selected = None
		self.hasErrors = False
		self.updateBoardMarkup()
	
	def setTxtStd(self, txt):
		txt.text_color = '#000'
		txt.background_color = '#fff'
		txt.font = ('<system>', 28)
		txt.border_color ='#ddd'
		txt.border_width = 1
		
	def setTxtGiven(self, txt):
		txt.background_color = '#f6f6f6'
		txt.border_color = '#ddd'
		txt.text_color = '#666'
		txt.font = ('<system-bold>', 28)
		txt.border_width = 1
		
	def setTxtSelected(self, txt):
		txt.background_color = '#91d4ff'
		txt.text_color = '#0e83ce'
		txt.border_color ='#0e83ce'
		txt.border_width = 3
		
	def setTxtHighlighted(self, txt):
		txt.background_color = '#eeffef'
		# txt.text_color = '#000'
		txt.border_color ='#bae8be'
		txt.border_width = 1
		
	def setTxtError(self, txt):
		txt.background_color = '#ffbbbb'
		txt.border_color = '#db5050'
		txt.text_color = '#db5050'
		
	def setTxtNumHighlighted(self, txt):
		self.setTxtHighlighted(txt)
		txt.border_width = 3
		
	def resetTxtField(self, r,c):
		if (r,c) in self.givens:
			self.setTxtGiven(self.txtGrid[c][r])
		else:
			self.setTxtStd(self.txtGrid[c][r])
	
	def resetBoard(self):
		for r in range(9):
			for c in range(9):
				self.resetTxtField(r,c)
		
	def initTxtField(self, txt, row, col):
		txt.keyboard_type = ui.KEYBOARD_NUMBER_PAD
		txt.bordered = False
		txt.alignment = ui.ALIGN_CENTER
		txt.delegate = self.makeCellDelegate(row, col)
		txt.text = ''
		self.setTxtStd(txt)
		
	def getNumClues(self):
		return len(self.givens)
		
	def getPuzStr(self):
		grid = ['.' for x in range(9*9)]
		for g in self.givens:
			grid[g[0]*9 + g[1]] = self.txtGrid[g[1]][g[0]].text
		return ''.join([str(c) for c in grid])
		
	def commitToGivens(self):
		for c in range(9):
			for r in range(9):
				txt = self.txtGrid[c][r]
				if txt.text != '':
					if (r,c) not in self.givens:
						self.givens.append((r,c))
		self.updateBoardMarkup()
		
	def uncommitGivens(self):
		self.givens = []
		self.updateBoardMarkup()
				
	def setGivens(self, puz):
		self.resetGrid()
		col = 0
		row = 0
		for c in puz:
			if c in '123456789':
				n = int(c)
				txt = self.txtGrid[col][row]
				txt.text = str(n)
				self.givens.append((row,col))
				self.setTxtGiven(txt)
			col += 1
			if col >= 9:
				col = 0
				row += 1
			if row == 8 and col > 8:
				break
		self.updateBoardMarkup()
				
	def setValues(self, puz):
		col = 0
		row = 0
		for c in puz:
			if c in '123456789' and (row,col) not in self.givens:
				n = int(c)
				txt = self.txtGrid[col][row]
				txt.text = str(n)
				self.setTxtStd(txt)
			col += 1
			if col >= 9:
				col = 0
				row += 1
		self.updateBoardMarkup()
				
	def setSelected(self, row=None, col=None):
		if row == None or col == None:
			self.selected = None
		else:
			self.selected = (row,col)
		self.updateBoardMarkup()
		
	def updateBoardMarkup(self):
		s = self.selected
		self.resetBoard()
		if s != None:
			tf = self.txtGrid[s[1]][s[0]]
			self.highlightAt(*s)
		self.markErrors()
		if s != None:
			self.setTxtSelected(tf)
		
	def highlightAt(self, row, col):
		# highlight column
		for r in range(9):
			if (r != row):
				self.setTxtHighlighted(self.txtGrid[col][r])
		# hughlight row
		for c in range(9):
			if (c != col):
				self.setTxtHighlighted(self.txtGrid[c][row])
		# highlight box
		br = row//3
		bc = col//3
		for r in range(br*3, br*3 + 3):
			for c in range(bc*3, bc*3 + 3):
				if r != row and c != col:
					self.setTxtHighlighted(self.txtGrid[c][r])
		# highlight numbers
		n = self.txtGrid[col][row].text
		if n != '':
			for r in range(9):
				for c in range(9):
					if r != row or c != col:
						if self.txtGrid[c][r].text == n:
							self.setTxtNumHighlighted(self.txtGrid[c][r])
		
	def markErrors(self):
		foundError = False
		# mark columns
		for c in range(9):
			ct = [0 for x in range(10)]
			for r in range(9):
				n = self.txtGrid[c][r].text
				if n != '':
					ct[int(n)] += 1
			for i in ct:
				if i > 1:
					foundError = True
					for r in range(9):
						self.setTxtError(self.txtGrid[c][r])
					break
		# mark rows
		for r in range(9):
			ct = [0 for x in range(10)]
			for c in range(9):
				n = self.txtGrid[c][r].text
				if n != '':
					ct[int(n)] += 1
			for i in ct:
				if i > 1:
					foundError = True
					for c in range(9):
						self.setTxtError(self.txtGrid[c][r])
					break
		# mark boxes
		for br in range(3):
			for bc in range(3):
				ct = [0 for x in range(10)]
				for r in range(br*3, br*3 + 3):
					for c in range(bc*3, bc*3 + 3):
						n = self.txtGrid[c][r].text
						if n != '':
							ct[int(n)] += 1
				for i in ct:
					if i > 1:
						foundError = True
						for r in range(br*3, br*3 + 3):
							for c in range(bc*3, bc*3 + 3):
								self.setTxtError(self.txtGrid[c][r])
						break
		self.hasErrors = foundError
				
	def makeCellDelegate(self, row, col):
		return self.CellDelegate(self, row, col)
		
	def end_editing(self):
		s = self.selected
		if s != None:
			self.txtGrid[s[1]][s[0]].end_editing()
				
				
				
	class CellDelegate (object):
		def __init__(self, outer, row, col):
			self.outer = outer
			self.row = row
			self.col = col
		def textfield_did_begin_editing(self, tf):
			self.outer.setSelected(self.row, self.col)
		def textfield_did_end_editing(self, tf):
			self.outer.setSelected()
		def textfield_should_change(self, tf, range, replacement):
			return not self.outer.selected in self.outer.givens
		def textfield_did_change(self, tf):
			if len(tf.text) > 1:
				tf.text = tf.text[-1]
			if len(tf.text) > 0 and tf.text[0] not in '123456789':
				tf.text = ''
			self.outer.updateBoardMarkup()
