import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Example(QWidget):
	def __init__(self):
		super().__init__()
		self.setGeometry(30, 30, 700, 400	)

		#self.setMouseTracking(True)
		
		#self.mouseMoveEvent = self.mouse_position
	'''
	def mouse_position(self, event):
		x = event.pos().x()
		y = event.pos().y()
		self.paintEvent()
		print(x,y)
	'''

	def paintEvent(self, event):
		painter = QPainter(self)
		pixmap = QPixmap("Images/Quart_top_View.jpg")
		painter.drawPixmap(self.rect(), pixmap)
		pen = QPen(Qt.red, 3)
		painter.setPen(pen)
		painter.drawLine(50, 55, self.rect().width()-45, 55)
		painter.drawLine(50, 357, self.rect().width()-45, 357)
		painter.drawLine(50, 357, self.rect().width()-650, 55)
		painter.drawLine(657, 357, self.rect().width()-43, 55)
		#painter.drawLine(10, 10, self.rect().width() -10 , 10)
		print(self.rect().width())

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())
