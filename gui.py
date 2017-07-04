#!/usr/bin/env python3	
# -*- coding: utf-8 -*-
 
import sys
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import cv2
import datetime
import time
 
 
class Webcam:
	def __init__(self):
		# Cargamos la GUI desde el archivo UI.
		self.MainWindow = uic.loadUi('gui.ui')

		# Tomamos el dispositivo de captura a partir de la webcam.
		self.webcam = cv2.VideoCapture(0)

		# Creamos un temporizador para que cuando se cumpla el tiempo limite tome una captura desde la webcam.
		self.timer = QtCore.QTimer(self.MainWindow);

		# Conectamos la señal timeout() que emite nuestro temporizador con la funcion show_frame().
		self.timer.timeout.connect(self.show_frame)

		# Tomamos una captura cada 1 mili-segundo.
		self.timer.start(1);

		self.MainWindow.TakePictureButton.clicked.connect(self.save_frame)
		
		#CalibrationPath = self.MainWindow.CalibrationPathLineEdit.text()
		self.MainWindow.CalibrationPathLineEdit.setText("Choose your path...")
			
		self.MainWindow.ChooseCalibrationPathButton.clicked.connect(self.choose_path)
        
        
	### CHOOSE PATH TO SAVE IMAGE AND CALIBRATION FILE ###
	def choose_path(self):
		
		cmd = "python3 Functions/FolderDialog.py"
		path = (subprocess.check_output(cmd, shell=True)).decode("utf-8")
		self.MainWindow.CalibrationPathLineEdit.setText(path)
        
        
        ### SAVE IMAGE FUNCTION ###
	def save_frame(self):
		ok, img = self.webcam.read()

		if self.MainWindow.CalibrationPathLineEdit.text()!="Choose your path...":
			savepath = self.MainWindow.CalibrationPathLineEdit.text().replace('\n','')+'/frame' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '.png'
			cv2.imwrite(savepath, img)
		else:
			savepath = 'frame' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '.png'
			cv2.imwrite(savepath, img)
		print(savepath)
		
	### SHOW IMAGE ON QLABEL WIDGET ###        
	def show_frame(self):
		# Tomamos una captura desde la webcam.
		ok, img = self.webcam.read()

		if not ok:
		    return

		# Creamos una imagen a partir de los datos.
		#
		# QImage
		# (
		#   Los pixeles que conforman la imagen,
		#   Ancho de de la imagen,
		#   Alto de de la imagen,
		#   Numero de bytes que conforman una linea (numero_de_bytes_por_pixel * ancho),
		#   Formato de la imagen
		# )
		# 
		# img.shape
		# (
		#   Alto,
		#   Ancho,
		#   Planos de color/canales/bytes por pixel
		# )
		image = QtGui.QImage(img, img.shape[1], img.shape[0], img.shape[1] * img.shape[2], QtGui.QImage.Format_RGB888)

		# Creamos un pixmap a partir de la imagen.
		# OpenCV entraga los pixeles de la imagen en formato BGR en lugar del tradicional RGB,
		# por lo tanto tenemos que usar el metodo rgbSwapped() para que nos entregue una imagen con
		# los bytes Rojo y Azul intercambiados, y asi poder mostrar la imagen de forma correcta.
		pixmap = QtGui.QPixmap()
		pixmap.convertFromImage(image.rgbSwapped())

		# Mostramos el QPixmap en la QLabel.
		self.MainWindow.lblWebcam.setPixmap(pixmap)


		self.MainWindow.lblWebcam.mousePressEvent = self.get_pixel_position


	### GET CLICKED PIXEL POSITION ###
	def get_pixel_position(self , event):
		x = event.pos().x()
		y = event.pos().y() 
		print(x,y)
 
if __name__ == "__main__":


	app = QtWidgets.QApplication(sys.argv)
	webcam = Webcam()
	webcam.MainWindow.show()
	app.exec_()

