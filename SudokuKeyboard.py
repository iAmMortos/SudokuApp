import ui, sound
import enum
from wrapper import WrapInstance

class KeyboardMode(enum.Enum):
	Pen = 0
	Pencil = 1

class SudokuKeyboard(ui.View):
	
	def __init__(self):
		v = ui.load_view('/'.join(__name__.split('.')),bindings={self.__class__.__name__:WrapInstance(self),'self':self})
		
	def did_load(self):
		self.grid = None
		self.mode = None
		self.curNotes = []
		self.spentNums = []
		self.givenSelected = False
		
		self.pen_font = ('Baskerville-Bold', 42)
		self.pencil_font = ('Chalkduster', 42)
		
		self.numBtns = [None for n in range(9)]
		for i in range(9):
			btn = self['b%s' % (i+1)]
			btn.tint_color = '#000'
			btn.border_color = '#64c800'
			btn.corner_radius = 10
			self.initBtn(btn, i+1)
			self.numBtns[i] = btn
			
		self.clearBtn = self['clrbtn']
		self.clearBtn.tint_color = '#f00'
		self.clearBtn.action= self.clearAction
		
		self.noteToggle = self['penpencil']
		self.noteToggle.action = self.noteToggleAction
		
		self.noteToggle.selected_index = 1
		self.setMode(KeyboardMode.Pencil)
		
	def initBtn(self, btn, n):
		btn.action = lambda e: self.touch(n)
		
	def setMode(self, mode):
		self.mode = mode
		self.update()
		
	def noteToggleAction(self, e):
		i = self.noteToggle.selected_index
		if i == 1:
			self.setMode(KeyboardMode.Pencil)
			sound.play_effect('ui:mouseclick1')
		else:
			self.setMode(KeyboardMode.Pen)
			sound.play_effect('ui:mouserelease1')
			
	def touch(self, n):
		if self.mode == KeyboardMode.Pen:
			sound.play_effect('ui:rollover3')
			self.curNotes = []
			self.grid.setSelectedNum(n)
		elif self.mode == KeyboardMode.Pencil:
			sound.play_effect('ui:rollover2')
			self.grid.toggleSelectedNote(n)
			
	def clearAction(self, e):
		sound.play_effect('ui:switch10')
		if self.mode == KeyboardMode.Pen:
			self.grid.clearSelectedNum()
		elif self.mode == KeyboardMode.Pencil:
			self.grid.clearSelectedNote()
			
	def update(self):
		if self.givenSelected:
			for btn in self.numBtns:
				btn.enabled = False
			self.clearBtn.enabled = False
			self.curNotes = []
		else:
			for btn in self.numBtns:
				btn.enabled = True
			self.clearBtn.enabled = True
			
		if self.mode == KeyboardMode.Pen:
			self.noteToggle.tint_color = '#f00'
			for i,btn in enumerate(self.numBtns):
				btn.font = self.pen_font
				btn.border_width = 0
				btn.background_color = (0,0,0,0)
				if i+1 in self.spentNums:
					btn.enabled = False
		elif self.mode == KeyboardMode.Pencil:
			self.noteToggle.tint_color = '#1aa5ff'
			for i,btn in enumerate(self.numBtns):
				btn.font = self.pencil_font
				if i+1 in self.curNotes:
					btn.border_width = 1
					btn.background_color = '#e2ffcc'
				else:
					btn.border_width = 0
					btn.background_color = (0,0,0,0)
					
	def setGivenSelected(self, given):
		self.givenSelected = given
		self.update()
					
	def setSpentNums(self, nums):
		self.spentNums = nums
		self.update()
	
	def setCurNotes(self, notes):
		self.curNotes = [int(n) for n in notes]
		self.update()
		
	def end_editing(self):
		self.setGivenSelected(True)
