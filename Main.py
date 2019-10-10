import time
import ui
import console
from DancingLinks import DancingLinks
from SudokuSolver import SudokuSolver
from SudokuGrid2 import SudokuGrid2
from SudokuKeyboard import SudokuKeyboard
from PuzzlePlayer import PuzzlePlayer



def addMainTableView(navView):
	tv = ui.TableView()
	tv.allows_multiple_selection = False
	tv.allows_selection = True
	lds = ui.ListDataSource([
		{'title':'Play Random Sudoku',
		 'image':ui.Image('emj:Game_Die'),
		 'accessory_type':'disclosure_indicator'},
		{'title':'Input Puzzle',
		 'image':ui.Image('emj:Memo'),
		 'accessory_type':'disclosure_indicator'},
		{'title':'Sudoku Solver',
		 'image':ui.Image('emj:Imp'),
		 'accessory_type':'disclosure_indicator'}
		])
	tv.data_source = lds
	tv.flex = 'WH'
	tv.name = 'Sudoku'
	navView.push_view(tv, False)
	
def setUpFadeIn(view):
	curtain = ui.View()
	curtain.background_color = '#000'
	curtain.flex = 'WH'
	curtain.frame = view.frame
	view.add_subview(curtain)
	view._curtain = curtain
	curtain.bring_to_front()
	
def fadeIn(view):
	def animate():
		view._curtain.alpha = 0
	ui.animate(animate, completion=lambda:view.remove_subview(view._curtain))
	


class Main(ui.View):
	def did_load(self):
		navView = self['nv']
		navView.navigation_bar_hidden = True
		addMainTableView(navView)



def main():
	console.clear()
	#v = ui.load_view('PuzzlePlayer')
	v = ui.load_view('SudokuSolver')
	# v = ui.load_view()
	setUpFadeIn(v)
	v.present(style='full_screen',
						hide_title_bar=True,
	          orientations=['portrait'])
	v.resized()
	fadeIn(v)

if __name__ == '__main__':
	main()
