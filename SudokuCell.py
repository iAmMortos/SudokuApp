import ui, sound
from wrapper import WrapInstance

class SudokuCell (ui.View):
	def __init__(self, grid, row, col):
		v = ui.load_view('/'.join(__name__.split('.')),bindings={self.__class__.__name__:WrapInstance(self),'self':self})
		
		self.parent = grid
		self.row = row
		self.col = col
		
		self.flex = 'WHLRTB'
		self.border_width = 1
		self.border_color = '#ddd'
		self.notes = []
		self.numSize = 57
		self.noteSize = 18
		
	def getNum(self):
		t = self.num.text
		if not t == '':
			return int(t)
		return None
		
	def did_load(self):
		self.num = self['num']
		self.notes1 = self['notes1']
		self.notes2 = self['notes2']
		self.num.text = ''
		self.notes1.text = ''
		self.notes2.text = ''
		
	def resized(self):
		h = self.frame[3]
		self.numSize = h*0.95
		self.num.font = ('<System>',self.numSize)
		self.noteSize = h*0.28
		f = ('DejaVuSansMono',self.noteSize)
		self.notes1.font = f
		self.notes2.font = f
		
	def addNote(self, n):
		if str(n) not in self.notes:
			self.notes.append(str(n))
			self.notes.sort()
			self.updateNotes()
		
	def removeNote(self, n):
		if str(n) in self.notes:
			self.notes.remove(str(n))
			self.updateNotes()
		
	def toggleNote(self, n):
		if str(n) in self.notes:
			self.notes.remove(str(n))
		else:
			self.notes.append(str(n))
			self.notes.sort()
		self.updateNotes()
		
	def setNotes(self, n):
		self.notes = n
		self.notes.sort()
		self.updateNotes()
			
	def updateNotes(self):
		self.notes1.text = ''.join(self.notes[:5])
		self.notes2.text = ''.join(self.notes[5:])
		
	def clearNotes(self):
		self.notes = []
		self.updateNotes()
		
	def setNum(self, n):
		self.clearNotes()
		self.num.text = str(n)
		self.notes1.alpha = 0
		self.notes2.alpha = 0
		
	def clearNum(self):
		self.num.text = ''
		self.notes1.alpha = 1
		self.notes2.alpha = 1
		
	def markStd(self):
		self.background_color = '#fff'
		self.border_color ='#ddd'
		self.border_width = 1
		self.num.text_color = '#000'
		self.num.font = ('<system>', self.numSize)
		
	def markGiven(self):
		self.background_color = '#f6f6f6'
		self.border_color = '#ddd'
		self.border_width = 1
		self.num.text_color = '#666'
		self.num.font = ('<system-bold>', self.numSize)
		
	def markSelected(self):
		self.background_color = '#91d4ff'
		self.border_color ='#0e83ce'
		self.border_width = 3
		self.num.text_color = '#0e83ce'
		
	def markHighlighted(self):
		self.background_color = '#eeffef'
		self.border_color ='#bae8be'
		self.border_width = 1
		
	def markError(self):
		self.background_color = '#ffbbbb'
		self.border_color = '#db5050'
		self.num.text_color = '#db5050'
		
	def markNumHighlighted(self):
		self.markHighlighted()
		self.border_width = 3
		
	def touch_began(self, touch):
		sound.play_effect('ui:rollover5')
		self.parent.touched(self)
