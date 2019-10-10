import ui
from Dialog import *
from DancingLinks import DancingLinks
from LoadingPage import showLoadingPage

class SudokuSolver(ui.View):
	def did_load(self):
		me = self
		self.sudokuGrid = self['sudoku_grid']
		self.sudokuGrid.resized()
		self.keys = self['keys']
		self.sudokuGrid.bindKeyboard(self.keys)
		self.clearBtn = self['clear_btn']
		self.solveBtn = self['solve_btn']
		self.puzTxt = self['puzzle_txt']
		self.puzTxt.delegate = PuzTxtDelegate(self.sudokuGrid)
		self.sudokuGrid.touchAction = lambda: me.puzTxt.end_editing()
		
		self.clearBtn.action = self.clearPuzzle
		self.solveBtn.action = self.solvePuzzle
		
		with open('puzzles/hardest_puz.txt') as f:
			self.sudokuGrid.setGivens(''.join(l.strip() for l in f.readlines()))
		
	def resized(self):
		self.sudokuGrid.height = self.sudokuGrid.width
		self.keys.y = self.sudokuGrid.y + self.sudokuGrid.height + 8
		
	def touch_began(self, touch):
		self.sudokuGrid.end_editing()
		self.puzTxt.end_editing()
		
	def clearPuzzle(self, e):
		self.sudokuGrid.end_editing()
		self.puzTxt.end_editing()
		self.sudokuGrid.resetGrid()
		self.puzTxt.text = ''
		
	def solvePuzzle(self, e):
		self.sudokuGrid.end_editing()
		self.puzTxt.end_editing()
		self.sudokuGrid.commitToGivens()
		if self.sudokuGrid.getNumClues() < 17:
			showErrorDialog('A valid sudoku puzzle must start with at least 17 numbers.')
			self.sudokuGrid.uncommitGivens()
			return
		if self.sudokuGrid.hasErrors:
			showErrorDialog('This puzzle breaks the basic rules of sudoku, and therefore has no solution.')
			self.sudokuGrid.uncommitGivens()
			return 
		dl = DancingLinks(9)
		dl.ingestPuzzle(self.sudokuGrid.getPuzStr())
		# showLoadingPage(dl)
		dl.solve()
		if dl.canceled:
			self.sudokuGrid.uncommitGivens()
			return
		else:
			if dl.numSolutions == 0:
				showErrorDialog('This puzzle has no solution.')
				self.sudokuGrid.uncommitGivens()
				return 
			if dl.numSolutions > 1:
				showWarningDialog('This puzzle does not have a unique solution, so it is invalid. One of these possible solutions will be displayed.')
			self.sudokuGrid.setValues(dl.solutionStr)
			self.puzTxt.text = self.sudokuGrid.getPuzStr()
		
	#def keyboard_frame_will_change(self, frame):
		#self.y = -1 * frame[3]
		
		


class PuzTxtDelegate (object):
	def __init__(self, sudGrid):
		self.sudGrid = sudGrid
	def textfield_should_change(self, tf, range, replacement):
		return True
	def textfield_did_change(self, tf):
		self.sudGrid.resetGrid()
		self.sudGrid.setValues(tf.text.strip())
