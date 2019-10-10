import ui
from enum import Enum

class DialogType(Enum):
	Error = 1
	Info = 2
	Warning = 3

class Dialog(ui.View):
	
	def did_load(self):
		self.button = self['btn']
		self.message = self['msg']
		self.icon = self['icon']
		self.title = self['title']
		
	def _set(self, title, message, type=DialogType.Info):
		self.button.action = lambda a: self.close()
		self.message.text = message
		self.title.text = title
		
		if type == DialogType.Info:
			self.icon.image = ui.Image('iob:information_circled_256')
		elif type == DialogType.Error:
			self.icon.image = ui.Image('iob:alert_256')
		elif type == DialogType.Warning:
			self.icon.image = ui.Image('iob:alert_circled_256')
		
def showDialog(title, message, type=DialogType.Info):
	v = ui.load_view('Dialog')
	v._set(title, message, type)
	v.present(style='full_screen', hide_title_bar=True)
	v.wait_modal()
	
def showErrorDialog(message, title='Error'):
	showDialog(title, message, DialogType.Error)
	
def showInfoDialog(message, title='Info'):
	showDialog(title, message, DialogType.Info)

def showWarningDialog(message, title='Warning'):
	showDialog(title, message, DialogType.Warning)
		
if __name__ == '__main__':
	showDialog('Hello World!', 'I am Taylor, making a cool modal view that I can use as a message dialog!!!', DialogType.Warning)
