#!/usr/bin/env python3	
# -*- coding: utf-8 -*-
 
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
import subprocess
import cv2
import datetime
import time
import numpy as np

class MainGUI:
	def __init__(self):
		self.MainWindow = uic.loadUi('gui.ui')
		
		#CalibrationPath = self.MainWindow.CalibrationPathLineEdit.text()
		self.MainWindow.CalibrationPathLineEdit.setText("Choose your path...")
		self.MainWindow.CourtImagePathLineEdit.setText("Choose your image...")			
		self.MainWindow.ChooseCourtImagePathButton.clicked.connect(self.choose_file)
		self.MainWindow.ChooseCalibrationPathButton.clicked.connect(self.choose_path)
		
		self.MainWindow.GetNewCalibrationButton.setEnabled(False)
		self.MainWindow.CalibrationPathLineEdit.textChanged.connect(self.get_calibration_button_state)		
		self.MainWindow.GetNewCalibrationButton.clicked.connect(self.camera_calibration)
		
		# SET QWIDGET PRINT ELIPSE ON POSITION
		label = Stadium(QPixmap("Images/Court_top_View.jpg"))
		self.MainWindow.TennisCourtImage.setLayout(QtWidgets.QVBoxLayout())
		self.MainWindow.TennisCourtImage.layout().addWidget(label)


	def get_calibration_button_state(self):
		if self.MainWindow.CalibrationPathLineEdit.text() != "Choose your path...":
			self.MainWindow.GetNewCalibrationButton.setEnabled(True)
		else:
			self.MainWindow.GetNewCalibrationButton.setEnabled(False)


	### CAMERA CALIBRATION SCRIPT ###
	def camera_calibration(self):
		#cmd = "Functions/camera_calibration"
		cmd = "python3 Functions/camera_calibration.py"
		path = (subprocess.check_output(cmd, shell=True)).decode("utf-8")
		 
	### CHOOSE PATH TO OPEN COURT FILE ###
	def choose_file(self):
		cmd = "python3 Functions/FileDialog.py"
		path = (subprocess.check_output(cmd, shell=True)).decode("utf-8")
		self.MainWindow.CourtImagePathLineEdit.setText(path)


	### CHOOSE PATH TO SAVE IMAGE AND CALIBRATION FILE ###
	def choose_path(self):
		cmd = "python3 Functions/FolderDialog.py"
		path = (subprocess.check_output(cmd, shell=True)).decode("utf-8")
		self.MainWindow.CalibrationPathLineEdit.setText(path)
        

class Stadium(QWidget):
	def __init__(self, pixmap, parent=None):
		QWidget.__init__(self, parent=parent)
		self.pixmap = pixmap
		self.pos = None
		self.setMouseTracking(True)

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.drawPixmap(self.rect(), self.pixmap)
		painter.setPen(QPen(Qt.blue, 20, Qt.SolidLine))
		if self.pos:
			painter.drawEllipse(self.pos, 10, 10)

	def mouseMoveEvent(self, event):
		self.pos = event.pos()
		#print(self.pos)
		self.update()

		
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	main_gui = MainGUI()
	main_gui.MainWindow.show()
	app.exec_()

