import sys,os
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
 
class App(QWidget):
 
	def __init__(self):
		super().__init__()
		self.title = 'Choose Path Dialog'
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.openFileNamesDialog()

		self.show()
	
	def openFileNameDialog(self):    
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		
		path = str(QFileDialog.getExistingDirectory(self,"Choose Folder"))
		
		print(path)
		'''
		if path:
			content = os.listdir(path)
			if "tomo.h5" and "tomo_flats.h5" and "tomo_dark_before.h5" in content:
				#print(content)
				print(path)
				
			else:
				print("Wrong folder, try again...")
		else:
			pass
			
		'''
			
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit()#app.exec_())
