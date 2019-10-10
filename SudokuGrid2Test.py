import ui
import console
from SudokuGrid2 import SudokuGrid2
from SudokuCell import SudokuCell
from DancingLinks import DancingLinks
from SudokuKeyboard import SudokuKeyboard

class SudokuGrid2Test (ui.View):
	def did_load(self):
		pass

if __name__ == '__main__':
	console.clear()
	v=ui.load_view()
	sg = v['sg']
	kb = v['kb']
	v.present(style='full_screen',
	          hide_title_bar=True,
	          orientations=['portrait'])
	v.touch_began = lambda t: sg.end_editing()
	dl = DancingLinks(9)
	dl.loadPuzzle('puzzles/hardest_puz.txt')
	sg.setGivens(dl.puzStr)
	sg.y += 14
	sg.height = sg.width
	sg.resized()
	kb.y = sg.y + sg.height + 6
	sg.bindKeyboard(kb)
