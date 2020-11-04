import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPixmap 
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
		QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
		QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
		QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit, QHBoxLayout,
		QVBoxLayout, QWidget, QMainWindow, QMessageBox)

import sys
import os
import numpy

class SummaryCanvas(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)

		self.compute_initial_figure()

		FigureCanvas.__init__(self, fig)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self,
								   QSizePolicy.Expanding,
								   QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		
	def compute_initial_figure(self):
		t = numpy.arange(0.0, 3.0, 0.01)
		s = numpy.power(t,2)
		self.axes.plot(t, s)

class QtSummaryWindow(QWidget):
	def __init__(self,master):
		super(QtSummaryWindow,self).__init__()
		self.master = master
		self.connection = self.master.connection
		self.GroupBoxSeg = [1, 1, 5, 1]
		self.checkboxs = []
		self.SiteList = ["All","OSU","Site 1", "Site2"]

		#Fixme: QTimer to be added to update the page automatically

		self.mainLayout = QGridLayout()
		self.setLayout(self.mainLayout)
		
		self.setUIGeometry()
		self.createHeadLine()
		self.createMain()
		self.createApp()
		self.occupied()

	def setUIGeometry(self):
		self.setGeometry(400, 400, 400, 400)  
		self.setWindowTitle('Summary')  
		self.show()

	def createHeadLine(self):
		self.HeadBox = QGroupBox()

		self.HeadLayout = QHBoxLayout()

		HeadLabel = QLabel('<font size="5"> Summary: Module test </font>')
		HeadFont=QFont()
		HeadFont.setBold(True)
		HeadLabel.setMaximumHeight(30)
		HeadLabel.setFont(HeadFont)

		self.HeadLayout.addWidget(HeadLabel)

		self.HeadBox.setLayout(self.HeadLayout)

		self.mainLayout.addWidget(self.HeadBox, sum(self.GroupBoxSeg[:0]), 0, self.GroupBoxSeg[0], 1)

	def destroyHeadLine(self):
		self.HeadBox.deleteLater()
		self.mainLayout.removeWidget(self.HeadBox)

	def createChecks(self):
		self.OptionBox = QGroupBox()
		CheckBoxLayout =  QHBoxLayout()
		
		for site in SiteList:
			checkBox = QCheckBox("&{0}".format(site))
			self.checkboxs.append(checkBox)
			CheckBoxLayout.addWidget(checkBox)

		self.OptionBox.setLayout(CheckBoxLayout)
		
		self.mainLayout.addWidget(self.OptionBox, sum(self.GroupBoxSeg[0:1]), 0, self.GroupBoxSeg[1], 1)
	
	def createMain(self):
		self.MainBodyBox = QGroupBox()

		mainbodylayout = QVBoxLayout()

		sc = SummaryCanvas(width=5, height=4, dpi=100)
		mainbodylayout.addWidget(sc)


		self.MainBodyBox.setLayout(mainbodylayout)
		self.mainLayout.addWidget(self.MainBodyBox, sum(self.GroupBoxSeg[0:2]), 0, self.GroupBoxSeg[2], 1)

	def destroyMain(self):
		self.MainBodyBox.deleteLater()
		self.mainLayout.removeWidget(self.MainBodyBox)

	def createApp(self):
		self.AppOption = QGroupBox()
		self.StartLayout = QHBoxLayout()

		self.ResetButton = QPushButton("&Reset")
		self.ResetButton.clicked.connect(self.destroyMain)
		self.ResetButton.clicked.connect(self.createMain)

		self.CloseButton = QPushButton("&Close")
		self.CloseButton.clicked.connect(self.release)
		self.CloseButton.clicked.connect(self.closeWindow)

		self.StartLayout.addStretch(1)
		self.StartLayout.addWidget(self.ResetButton)
		self.StartLayout.addWidget(self.CloseButton)
		self.AppOption.setLayout(self.StartLayout)

		self.mainLayout.addWidget(self.AppOption, sum(self.GroupBoxSeg[0:3]), 0, self.GroupBoxSeg[3], 1)

	def destroyApp(self):
		self.AppOption.deleteLater()
		self.mainLayout.removeWidget(self.AppOption)

	def closeWindow(self):
		self.release()
		self.close()

	def occupied(self):
		self.master.SummaryButton.setDisabled(True)

	def release(self):
		self.master.SummaryButton.setDisabled(False)

	

	

