import ui
import time
from threading import Thread

class LoadingPage(ui.View):
	def __init__(self):
		self.cancelable = None
		
	def did_load(self):
		self.loadAnimTxt = self['loadanim']
		self.running = True
		self.cancelBtn = self['cancelbtn']
		self.cancelBtn.action = self.cancelAction
		self.elapsedTxt = self['elapsed']
		self.loop()
		
	@ui.in_background
	def loop(self):
		idx = 0
		frames = '\|/—/|\—'
		# wait for this view to finish its "present" animation before starting its child process. Otherwise, if this process finishes REALLY quickly and 'finished' is called, close() won't do anything and it'll just sit there.
		time.sleep(.5)
		t = Thread(target=self.cancelable.start)
		t.start()
		starttime = time.time()
		while self.running:
			curtime = time.time()
			self.loadAnimTxt.text = frames[idx]
			idx = (idx + 1) % len(frames)
			self.elapsedTxt.text = 'Elapsed Time: %d seconds' % (curtime - starttime)
			time.sleep(1/8)
			
	def finished(self):
		self.running = False
		self.close()
			
	def cancelAction(self, e):
		self.running = False
		self.cancelable.cancel()
		self.close()
		
	def _set(self, cancelable):
		self.cancelable = cancelable
		self.cancelable.registerListener(self)
		
		
		
def showLoadingPage(cancelable):
	v = ui.load_view()
	v._set(cancelable)
	v.present(style='full_screen', hide_title_bar=True)
	v.wait_modal()
		
if __name__ == '__main__':
	v = ui.load_view()
	v.present()
