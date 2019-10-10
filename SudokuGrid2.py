import ui
from SudokuCell import SudokuCell


def generate_cell(grid,r,c):
	s = 32
	x = s*c + 2*(c//3)
	y = s*r + 2*(r//3)
	cell = SudokuCell(grid, r, c)
	cell.frame = (x,y,s,s)
	cell.clearNotes()
	cell.clearNum()
	return cell
	
def generate_separator(d,n):
	lbl = ui.Label()
	lbl.background_color = '#666'
	lbl.width = 292 if d=='h' else 2
	lbl.height = 292 if d=='v' else 2
	lbl.x = 0 if d=='h' else (n*3*32 + (n-1)*2)
	lbl.y = 0 if d=='v' else (n*3*32 + (n-1)*2)
	lbl.flex = ('W' if d=='h' else 'H') + 'LRTB'
	return lbl

class SudokuGrid2 (ui.View):
	
	def __init__(self):
		self.frame = (0,0,292,292)
		self.keyboard = None
		self.txtGrid = [[None for x in range(9)] for x in range(9)]
		self.touchAction = None
		self.changeListeners = []
		for c in range(9):
			for r in range(9):
				cell = generate_cell(self, r,c)
				self.add_subview(cell)
				self.txtGrid[c][r] = cell
		self.add_subview(generate_separator('h',1))
		self.add_subview(generate_separator('h',2))
		self.add_subview(generate_separator('v',1))
		self.add_subview(generate_separator('v',2))
		self.border_width = 2
		self.border_color = '#666'
		self.resetGrid(True, notify=False)
				
	def resetGrid(self, first=False, notify=True):
		if not first:
			for c in range(9):
				for r in range(9):
					self.txtGrid[c][r].clearNum()
					self.txtGrid[c][r].clearNotes()
		self.givens = []
		self.resetUsedNums()
		self.selected = None
		self.hasErrors = False
		self.updateBoardMarkup()
		if notify:
			self.notifyChangeListeners()
		
	def clearCellMarkup(self, r,c):
		if (r,c) in self.givens:
			self.txtGrid[c][r].markGiven()
		else:
			self.txtGrid[c][r].markStd()
	
	def clearMarkup(self):
		for r in range(9):
			for c in range(9):
				self.clearCellMarkup(r,c)
		
	def getNumClues(self):
		return len(self.givens)
		
	def getPuzStr(self):
		grid = ['.' for x in range(9*9)]
		for g in self.givens:
			grid[g[0]*9 + g[1]] = self.txtGrid[g[1]][g[0]].getNum()
		return ''.join([str(c) for c in grid])
		
	def commitToGivens(self, notify=True):
		for c in range(9):
			for r in range(9):
				cell = self.txtGrid[c][r]
				if cell.getNum() != None:
					if (r,c) not in self.givens:
						self.givens.append((r,c))
		self.updateBoardMarkup()
		if notify:
			self.notifyChangeListeners()
		
	def uncommitGivens(self, notify=True):
		self.givens = []
		self.updateBoardMarkup()
		if notify:
			self.notifyChangeListeners()
				
	def setGivens(self, puz, notify=True):
		self.resetGrid(notify=False)
		col = 0
		row = 0
		for c in puz:
			if c in '123456789':
				n = int(c)
				self.addUsedNum(n)
				cell = self.txtGrid[col][row]
				cell.setNum(n)
				self.givens.append((row,col))
				cell.markGiven()
			col += 1
			if col >= 9:
				col = 0
				row += 1
			if row == 8 and col > 8:
				break
		self.updateBoardMarkup()
		if notify:
			self.notifyChangeListeners()
				
	def setValues(self, puz, notify=True):
		col = 0
		row = 0
		for c in puz:
			if c in '123456789' and (row,col) not in self.givens:
				n = int(c)
				cell = self.txtGrid[col][row]
				if cell.getNum() != None:
					self.removeUsedNum(cell.getNum())
				self.addUsedNum(n)
				cell.setNum(n)
				cell.markStd()
			col += 1
			if col >= 9:
				col = 0
				row += 1
		self.updateBoardMarkup()
		if notify:
			self.notifyChangeListeners()
			
	def setNotes(self, notes, notify=True):
		for i,note in enumerate(notes):
			if note != []:
				r,c = i//9,i%9
				self.txtGrid[c][r].setNotes(note)
		if notify:
			self.notifyChangeListeners()
		self.updateBoardMarkup()
			
	def clearValues(self, notify=True):
		for r in range(9):
			for c in range(9):
				if (r,c) not in self.givens:
					self.txtGrid[c][r].clearNum()
		if notify:
			self.notifyChangeListeners()
		self.updateBoardMarkup()
			
	def clearNotes(self, notify=True):
		for r in range(9):
			for c in range(9):
				if (r,c) not in self.givens:
					self.txtGrid[c][r].clearNotes()
		if notify:
			self.notifyChangeListeners()
		self.updateBoardMarkup()
			
	def resetPuzzle(self, notify=True):
		self.clearNotes(notify=False)
		self.clearValues(notify=False)
		if notify:
			self.notifyChangeListeners()
		self.updateBoardMarkup()
				
	def setSelected(self, cell=None):
		if cell == None:
			self.selected = None
		else:
			self.selected = (cell.row, cell.col)
			if self.selected in self.givens:
				self.keyboard.setGivenSelected(True)
			else:
				self.keyboard.setGivenSelected(False)
				self.keyboard.setCurNotes(cell.notes)
		self.updateBoardMarkup()
		
	def updateBoardMarkup(self):
		s = self.selected
		self.clearMarkup()
		if s != None:
			cell = self.txtGrid[s[1]][s[0]]
			self.highlightAt(*s)
		self.markErrors()
		if s != None:
			cell.markSelected()
		
	def highlightAt(self, row, col):
		# highlight column
		for r in range(9):
			if (r != row):
				self.txtGrid[col][r].markHighlighted()
		# hughlight row
		for c in range(9):
			if (c != col):
				self.txtGrid[c][row].markHighlighted()
		# highlight box
		br = row//3
		bc = col//3
		for r in range(br*3, br*3 + 3):
			for c in range(bc*3, bc*3 + 3):
				if r != row and c != col:
					self.txtGrid[c][r].markHighlighted()
		# highlight numbers
		n = self.txtGrid[col][row].getNum()
		if n != None:
			for r in range(9):
				for c in range(9):
					if r != row or c != col:
						if self.txtGrid[c][r].getNum() == n:
							self.txtGrid[c][r].markNumHighlighted()
		
	def markErrors(self):
		foundError = False
		# mark columns
		for c in range(9):
			ct = [0 for x in range(10)]
			for r in range(9):
				n = self.txtGrid[c][r].getNum()
				if n != None:
					ct[n] += 1
			for i in ct:
				if i > 1:
					foundError = True
					for r in range(9):
						self.txtGrid[c][r].markError()
					break
		# mark rows
		for r in range(9):
			ct = [0 for x in range(10)]
			for c in range(9):
				n = self.txtGrid[c][r].getNum()
				if n != None:
					ct[n] += 1
			for i in ct:
				if i > 1:
					foundError = True
					for c in range(9):
						self.txtGrid[c][r].markError()
					break
		# mark boxes
		for br in range(3):
			for bc in range(3):
				ct = [0 for x in range(10)]
				for r in range(br*3, br*3 + 3):
					for c in range(bc*3, bc*3 + 3):
						n = self.txtGrid[c][r].getNum()
						if n != None:
							ct[n] += 1
				for i in ct:
					if i > 1:
						foundError = True
						for r in range(br*3, br*3 + 3):
							for c in range(bc*3, bc*3 + 3):
								self.txtGrid[c][r].markError()
						break
		self.hasErrors = foundError
				
	def end_editing(self):
		s = self.selected
		if s != None:
			self.setSelected()
		self.keyboard.end_editing()
			
	def resized(self):
		for c in range(9):
			for r in range(9):
				self.txtGrid[c][r].resized()
				
	def touched(self, cell):
		self.setSelected(cell)
		if self.touchAction:
			self.touchAction()
		
	def setSelectedNum(self, n, notify=True):
		if self.selected != None and self.selected not in self.givens:
			cell = self.txtGrid[self.selected[1]][self.selected[0]]
			if cell.getNum() != None:
				self.removeUsedNum(cell.getNum())
			self.addUsedNum(n)
			cell.setNum(n)
			self.removeFromNeighborNotes(cell)
			self.updateBoardMarkup()
			if notify:
				self.notifyChangeListeners()
			
	def clearSelectedNum(self, notify=True):
		if self.selected != None and self.selected not in self.givens:
			cell = self.txtGrid[self.selected[1]][self.selected[0]]
			if cell.getNum() != None:
				self.removeUsedNum(cell.getNum())
			cell.clearNum()
			self.updateBoardMarkup()
			if notify:
				self.notifyChangeListeners()
			
	def toggleSelectedNote(self, n, notify=True):
		if self.selected != None and self.selected not in self.givens:
			cell = self.txtGrid[self.selected[1]][self.selected[0]]
			cell.toggleNote(n)
			self.keyboard.setCurNotes(cell.notes)
			if notify:
				self.notifyChangeListeners()
		
	def clearSelectedNote(self, notify=True):
		if self.selected != None and self.selected not in self.givens:
			cell = self.txtGrid[self.selected[1]][self.selected[0]]
			cell.clearNotes()
			self.keyboard.setCurNotes(cell.notes)
			if notify:
				self.notifyChangeListeners()
			
	def bindKeyboard(self, keyboard):
		self.keyboard = keyboard
		keyboard.grid = self
		keyboard.setGivenSelected(True)
		
	def addUsedNum(self, n):
		self.numCount[n-1] += 1
		spent = []
		for i,n in enumerate(self.numCount):
			if n >= 9:
				spent.append(i+1)
		if self.keyboard:
			self.keyboard.setSpentNums(spent)
		
	def removeUsedNum(self, n):
		self.numCount[n-1] -= 1
		spent = []
		for i,n in enumerate(self.numCount):
			if n >= 9:
				spent.append(i+1)
		if self.keyboard:
			self.keyboard.setSpentNums(spent)
		
	def resetUsedNums(self):
		self.numCount = [0 for x in range(9)]
		if self.keyboard:
			self.keyboard.setSpentNums([])
			
	def removeFromNeighborNotes(self, cell):
		r,c,n = cell.row, cell.col, cell.getNum()
		for ci in range(9):
			if ci is not c:
				self.txtGrid[ci][r].removeNote(n)
		for ri in range(9):
			if ri is not r:
				self.txtGrid[c][ri].removeNote(n)
		bc = c // 3
		br = r // 3
		for ci in range (bc*3, bc*3+3):
			for ri in range (br*3, br*3+3):
				if ci is not c or ri is not r:
					self.txtGrid[ci][ri].removeNote(n)
					
	def addChangeListener(self, listener):
		self.changeListeners.append(listener)
		
	def removeChangeListener(self, listener):
		self.changeListeners.remove(listener)
		
	def notifyChangeListeners(self):
		for l in self.changeListeners:
			l()
					
	def saveGrid(self, path):
		s = ''
		for r in range(9):
			for c in range(9):
				cell = self.txtGrid[c][r]
				line = ''
				if (r,c) in self.givens:
					line = '!%s\n' % cell.getNum()
				elif cell.getNum() != None:
					line = '%s\n' % cell.getNum()
				elif len(cell.notes) > 0:
					line = '*%s\n' % ''.join(cell.notes)
				else:
					line = '_\n'
				s += line
		with open(path, 'w') as f:
			f.writelines(s)
			
	def loadGrid(self, path, notify=True):
		self.resetGrid(notify=False)
		lines = []
		givens = ['.' for x in range(81)]
		nums = ['.' for x in range(81)]
		notes = [[] for x in range(81)]
		with open(path, 'r') as f:
			lines = [l.strip() for l in f.readlines()]
		for i,line in enumerate(lines):
			if line.startswith('!'):
				givens[i] = line[1:]
			elif line.startswith('*'):
				notes[i] = list(line[1:])
			elif line in '123456789':
				nums[i] = line
		self.setGivens(''.join(givens), notify=False)
		self.setValues(''.join(nums), notify=False)
		self.setNotes(notes, notify=False)
		if notify:
			self.notifyChangeListeners()
