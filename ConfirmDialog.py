import ui
from enum import Enum



class ConfirmDialogResult(Enum):
	Ok = 1
	Cancel= 2
	
	

class ConfirmDialog (ui.View):
	
	def did_load(self):
		self.okBtn = self['okbtn']
		self.cancelBtn = self['cnclbtn']
		self.message = self['msg']
		self.result = None
		
		self.okBtn.action = self.okAction
		self.cancelBtn.action = self.cancelAction

	def _set(self, message):
		self.message.text = message
		
	def okAction(self, e):
		self.result = ConfirmDialogResult.Ok
		self.close()
		
	def cancelAction(self, e):
		self.result = ConfirmDialogResult.Cancel
		self.close()
		
def showConfirmDialog(message):
	v = ui.load_view('ConfirmDialog')
	v._set(message)
	v.present(style='full_screen', hide_title_bar=True)
	v.wait_modal()
	return v.result
