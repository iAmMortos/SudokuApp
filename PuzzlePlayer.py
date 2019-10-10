import ui
import os
from DancingLinks import DancingLinks
from ConfirmDialog import *

_defaultPath = 'saved/player.puz'

class PuzzlePlayer(ui.View):
	def did_load(self):
		me = self
		self.kb = self['kb']
		self.sg = self['sg']
		self.sg.resized()
		self.sg.bindKeyboard(self.kb)
		self.sg.addChangeListener(lambda: me.sg.saveGrid(_defaultPath))
		self['genbtn'].action = self.generate
		self['clrbtn'].action = self.clear
		
		if os.path.exists(_defaultPath):
			self.sg.loadGrid(_defaultPath)
		else:
			self.generate()
		
	def resized(self):
		self.sg.height = self.sg.width
		self.kb.y = self.sg.y + self.sg.height + 8
		
	def generate(self, a=None):
		pass
		#self.sg.setValues(dl.solutionStr)
		#with open('puzzles/easy_puz.txt') as f:
			#self.sg.setGivens(''.join(l.strip() for l in f.readlines()))
		
		
	def clear(self, a=None):
		r = showConfirmDialog('Are you sure you want to erase your progress?')
		if r == ConfirmDialogResult.Ok:
			self.sg.resetPuzzle()
		
	def touch_began(self, t):
		self.sg.end_editing()
