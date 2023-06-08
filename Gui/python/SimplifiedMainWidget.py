#5-19 test the code, to see if it can enter the interface, if yes then fix the LED issue after check the power for plta

#5-19 error no attribute 'powerStatusValue'

#5- 24: ryan we probabaly dont need the read temp and print it. Instead we to read the data at the background and kill the program if it exceed certain value
# moving the setup up at top of __init__ it start to send message but powerstatusvalue issue is still exist

#5-25 fix LED, add quit signal that do the power toggle(closeEvent() in SimplifiedMain()) when quit

#6-1 debug to run test see "self.firmwareDescription = self.BeBoardWidget.getFirmwareDescription()" being run
from PyQt5 import QtCore
from PyQt5 import QtSerialPort
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPixmap, QPalette,  QImage, QIcon
from PyQt5.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox, QDateTimeEdit,
		QDial, QDialog, QFormLayout, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
		QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
		QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit, QHBoxLayout,
		QVBoxLayout, QWidget, QMainWindow, QMessageBox)

import pyvisa as visa
import subprocess

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from Gui.QtGUIutils.QtRunWindow import *
from Gui.QtGUIutils.QtFwCheckDetails import *
from Gui.python.CustomizedWidget import *
from Gui.python.Firmware import *
from Gui.GUIutils.DBConnection import *
from Gui.GUIutils.FirmwareUtil import *
from Gui.GUIutils.settings import *
from Gui.python.ArduinoWidget import *
from Gui.python.Peltier import *

class SimplifiedMainWidget(QWidget):


	polaritySignal = pyqtSignal(list)
	tempReading = pyqtSignal(float)
	powerReading = pyqtSignal(int)
	setTempSignal = pyqtSignal(float)


	def __init__(self, master):
		super().__init__()
		self.setup()
		self.master = master
		self.connection = self.master.connection
		self.LVpowersupply = self.master.LVpowersupply
		self.HVpowersupply = self.master.HVpowersupply
		self.TryUsername = self.master.TryUsername
		self.DisplayedPassword = self.master.DisplayedPassword
		self.mainLayout = QGridLayout()
		self.setLayout(self.mainLayout)
		redledimage = QImage("icons/led-red-on.png").scaled(QSize(60,10), Qt.KeepAspectRatio, Qt.SmoothTransformation)
		self.redledpixmap = QPixmap.fromImage(redledimage)
		greenledimage = QImage("icons/green-led-on.png").scaled(QSize(60,10), Qt.KeepAspectRatio, Qt.SmoothTransformation)
		self.greenledpixmap = QPixmap.fromImage(greenledimage)
		self.createLogin()
		self.setupMainUI()
		#self.createLogin()

		#for peltier controller
		
		


	def setup(self):
		try:
			self.pelt = PeltierSignalGenerator()
			#self.buttonEnable.connect(self.enableButtons)
			self.polaritySignal.connect(self.setPolarityStatus)

			# These should emit signals
			self.pelt.sendCommand(self.pelt.createCommand('Set Type Define Write', ['0','0','0','0','0','0','0','0'])) # Allows set point to be set by computer software
			self.pelt.sendCommand(self.pelt.createCommand('Control Type Write', ['0','0','0','0','0','0','0','1'])) # Temperature should be PID controlled
			#add set temperature
			#self.convertSetTempValueToList(5)
			self.setTemp() #5 c now
			self.pelt.sendCommand(self.pelt.createCommand('Power On/Off Write' ,['0','0','0','0','0','0','0','1'])) # Turn on the power by default
			self.powerStatusValue = 1
			

			self.pelt.sendCommand(self.pelt.createCommand('Proportional Bandwidth Write', ['0','0','0','0','0','0', 'c', '8'])) # Set proportional bandwidth
			message, _= self.pelt.sendCommand(self.pelt.createCommand('Control Output Polarity Read', ['0','0','0','0','0','0','0','0']))

			#self.buttonEnable.emit()
			self.polaritySignal.emit(message)

			time.sleep(1) # Needed to avoid collision with temperature and power reading

			#Start temperature and power monitoring

			# Create QTimer that will call functions
			self.timer = QTimer()
			self.timer.timeout.connect(self.controllerMonitoring)
			#self.tempReading.connect(lambda temp: self.currentTempDisplay.display(temp))   #we need to read it but not to display the color
			self.power = 1 
			self.powerReading.connect(lambda power: self.setPowerStatus(power)) 
			self.timer.start(500) # Perform monitoring functions every 500ms



		except Exception as e:
			print(e)
			print("Error while attempting to setup Peltier Controller: ", e)
		

	#new note: I add a default value to the Power, such that I want to the code to run
	# without touching the powerToggle	
	def setPowerStatus(self, power=0):
		if power == 1:
			self.PeltierMonitorValue.setPixmap(self.greenledpixmap) #means power on
			self.powerStatusValue =1

		elif power == 0:
			self.PeltierMonitorValue.setPixmap(self.redledpixmap) # means power off
			self.powerStatusValue =0
		else:
			print("Unkown power status")
		
	#note for powerToggle intially under local expert mode this method should
	#be excuted once I click the power on/off button. But right now we
	#it to run automatically?

	#new additional condition: set temperature is above current dew point (TBD)
	
	def powerToggle(self):
		
		if self.powerStatusValue == 0:
			try:
				self.pelt.sendCommand(self.pelt.createCommand('Power On/Off Write', ['0','0','0','0','0','0','0','1']))
			except Exception as e:
				print("Could not turn on controller due to error: ", e)
		elif self.powerStatusValue == 1:
			try:
				self.pelt.sendCommand(self.pelt.createCommand('Power On/Off Write', ['0','0','0','0','0','0','0','0']))
			except Exception as e:
				print("Could not turn off controller due to error: " , e)

	def setPolarityStatus(self, polarity):
		if polarity[8] == '0':
			self.polarityValue = 'HEAT WP1+ and WP2-'
			#self.polarityButton.setText(self.polarityValue)
		elif polarity[8] == '1':
			self.polarityValue = 'HEAT WP2+ and WP1-'
			#self.polarityButton.setText(self.polarityValue)
		else:
			print("Unexpected value sent back from polarity change function")

	def polarityToggle(self):
		if self.polarityValue == 'HEAT WP1+ and WP2-':
			polarityCommand = '1'
			self.polarityValue = 'HEAT WP2+ and WP1-'
		elif self.polarityValue == 'HEAT WP2+ and WP1-':
			polarityCommand = '0'
			self.polarityValue = 'HEAT WP1+ and WP2-'
		else:
			print('Unexpected value read for polarity')
			return
		self.pelt.sendCommand(self.pelt.createCommand('Control Output Polarity Write', ['0','0','0','0','0','0','0', polarityCommand]))
		self.polarityButton.setText(self.polarityValue) #FIXME Probably a better idea to read polarity from controller



	def setTemp(self)-> None:
		try:

			#message = self.convertSetTempValueToList(self.setTempInput.value())
			message = self.convertSetTempValueToList(5) # set the tempearature to 5 C by default for peltier controller
		


			self.pelt.sendCommand(self.pelt.createCommand('Fixed Desired Control Setting Write', message))
			time.sleep(0.5) # Sleep to make sure controller has time to set temperature

			message , _ = self.pelt.sendCommand(self.pelt.createCommand('Fixed Desired Control Setting Read', ['0','0','0','0','0','0','0','0']))
			message = self.convertSetTempListToValue(message)

			self.setTempSignal.emit(message)

		except Exception as e:
			print("Could not set Temperature: " , e)
			#self.currentSetTemp.setText("N/a")

	
	
	
	def convertSetTempListToValue(self, temp: list)-> float:
		temp = temp[1:9]
		temp = "".join(temp)
		temp = int(temp, 16)/100
		if temp > 1000:
			temp =  -1 * self.pelt.twosCompliment(temp)
		return temp
	def convertSetTempValueToList(self, temp: float) -> list:
		value = ['0','0','0','0','0','0','0','0']
		temp *= 100
		temp = int(temp)
		if temp < 0:
			temp = self.pelt.twosCompliment(temp)
		temp = self.pelt.convertToHex(temp)
		temp = self.pelt.stringToList(temp)
		cutoff = temp.index('x')
		temp = temp[cutoff+1:]
		for i, _ in enumerate(temp):
			value[-(i+1)] = temp[-(i+1)]
		return value


	def shutdown(self):
		try:
			self.pelt.sendCommand(self.pelt.createCommand('Power On/Off Write', ['0','0','0','0','0','0','0','0']))
		except Exception as e:
			print("Could not turn off controller due to error: " , e)

		try:
			self.tempPower.readTemp = False
		except AttributeError:
			pass

	def controllerMonitoring(self):
		try:
			message, passed = self.pelt.sendCommand(self.pelt.createCommand('Input1', ['0','0','0','0','0','0','0','0']))
			temp = "".join(message[1:9])
			temp = int(temp,16)/100
			self.tempReading.emit(temp)

			power, passed = self.pelt.sendCommand(self.pelt.createCommand('Power On/Off Read' ,['0','0','0','0','0','0','0','0']))
			self.powerReading.emit(int(power[8]))
			return
		except Exception as e:
			print(f"Could not read power/temperature due to error: {e}")
			return    


	
	#--------------------------------- end of PLTA control codes


	#self.SimpModBox = SimpleModuleBox()
	def createLogin(self):
		self.LoginGroupBox = QGroupBox("")
		self.LoginGroupBox.setCheckable(False)

		TitleLabel = QLabel('<font size="12"> Phase2 Pixel Module Test </font>')
		TitleLabel.setFont(QFont("Courier"))
		TitleLabel.setMaximumHeight(30)

		UsernameLabel = QLabel("Username:")
		self.UsernameEdit = QLineEdit('')
		self.UsernameEdit.setEchoMode(QLineEdit.Normal)
		self.UsernameEdit.setPlaceholderText(self.TryUsername)
		self.UsernameEdit.setMinimumWidth(220)
		self.UsernameEdit.setMaximumWidth(260)
		self.UsernameEdit.setMaximumHeight(30)
		self.UsernameEdit.setReadOnly(True)

		PasswordLabel = QLabel("Password:")
		self.PasswordEdit = QLineEdit('')
		self.PasswordEdit.setEchoMode(QLineEdit.Password)
		self.PasswordEdit.setPlaceholderText(self.DisplayedPassword)
		self.PasswordEdit.setMinimumWidth(220)
		self.PasswordEdit.setMaximumWidth(260)
		self.PasswordEdit.setMaximumHeight(30)
		self.PasswordEdit.setReadOnly(True)


		layout = QGridLayout()
		layout.setSpacing(20)
		layout.addWidget(TitleLabel,0,1,1,3,Qt.AlignCenter)
		layout.addWidget(UsernameLabel,1,1,1,1,Qt.AlignCenter)
		layout.addWidget(self.UsernameEdit,1,2,1,2)
		layout.addWidget(PasswordLabel,2,1,1,1,Qt.AlignCenter)
		layout.addWidget(self.PasswordEdit,2,2,1,2)

		#layout.setRowMinimumHeight(6, 50)

		layout.setColumnStretch(0, 1)
		layout.setColumnStretch(1, 1)
		layout.setColumnStretch(2, 2)
		layout.setColumnStretch(3, 1)
		self.LoginGroupBox.setLayout(layout)


		self.LogoGroupBox = QGroupBox("")
		self.LogoGroupBox.setCheckable(False)
		self.LogoGroupBox.setMaximumHeight(100)

		self.LogoLayout = QHBoxLayout()
		OSULogoLabel = QLabel()
		OSUimage = QImage("icons/osuicon.jpg").scaled(QSize(200,60), Qt.KeepAspectRatio, Qt.SmoothTransformation)
		OSUpixmap = QPixmap.fromImage(OSUimage)
		OSULogoLabel.setPixmap(OSUpixmap)
		CMSLogoLabel = QLabel()
		CMSimage = QImage("icons/cmsicon.png").scaled(QSize(200,60), Qt.KeepAspectRatio, Qt.SmoothTransformation)
		CMSpixmap = QPixmap.fromImage(CMSimage)
		CMSLogoLabel.setPixmap(CMSpixmap)
		
		self.LogoLayout.addWidget(OSULogoLabel)
		self.LogoLayout.addStretch(1)
		self.LogoLayout.addWidget(CMSLogoLabel)

		self.LogoGroupBox.setLayout(self.LogoLayout)

		self.mainLayout.addWidget(self.LoginGroupBox, 0, 0)




	def setupMainUI(self):
		##################################
		##  Testing some things out #######
		##################################
		self.simplifiedStatusBox = QGroupBox("Hello, {}!".format(self.TryUsername))
		
		
		statusString, colorString = checkDBConnection(self.connection)
		self.DBStatusLabel = QLabel()
		self.DBStatusLabel.setText("Database connection:")
		self.DBStatusValue = QLabel()
		if 'offline' in statusString:
			self.DBStatusValue.setPixmap(self.redledpixmap)
		else:
			self.DBStatusValue.setPixmap(self.greenledpixmap)
		
		#self.DBStatusValue.setText(statusString)
		#self.DBStatusValue.setStyleSheet(colorString)

		self.RefreshButton = QPushButton("&Refresh")
		self.RefreshButton.clicked.connect(self.checkDevices)


		self.HVPowerStatusLabel = QLabel()
		self.HVPowerStatusValue = QLabel()
		self.LVPowerStatusLabel = QLabel()
		self.LVPowerStatusValue = QLabel()
		
		self.ModuleEntryBox = QGroupBox("Please scan module QR code")
		ModuleEntryLayout = QGridLayout()

		SerialLabel = QLabel("SerialNumber:")
		self.SerialEdit = QLineEdit()

		CableLabel = QLabel("CableNumber")
		self.CableEdit = QLineEdit()

		#Selecting default HV
		self.HVpowersupply.setPowerModel(defaultHVModel[0])
		self.HVpowersupply.setInstrument(defaultUSBPortHV[0])
		statusString = self.HVpowersupply.getInfo()
		self.HVPowerStatusLabel.setText("HV status")
		
		self.HVPowerStatusValue.setPixmap(self.redledpixmap)
		if statusString != "No valid device" and statusString != None:
			self.HVPowerStatusValue.setPixmap(self.greenledpixmap)
			
		else:
			self.HVPowerStatusValue.setPixmap(self.redledpixmap)
			
		time.sleep(0.5)
		#Selecting default LV
		self.LVpowersupply.setPowerModel(defaultLVModel[0])
		self.LVpowersupply.setInstrument(defaultUSBPortLV[0])
		statusString = self.LVpowersupply.getInfo()
		self.LVPowerStatusLabel.setText("LV status")
		if statusString != "No valid device" and statusString != None:
			self.LVPowerStatusValue.setPixmap(self.greenledpixmap)
		else:
			self.LVPowerStatusValue.setPixmap(self.redledpixmap)

		self.StatusList = []
		self.StatusList.append([self.DBStatusLabel, self.DBStatusValue])
		self.StatusList.append([self.HVPowerStatusLabel, self.HVPowerStatusValue])
		self.StatusList.append([self.LVPowerStatusLabel, self.LVPowerStatusValue])

		self.FC7NameLabel = QLabel()
		self.FC7NameLabel.setText(defaultFC7)
		self.FC7StatusValue = QLabel()

		firmwareName, fwAddress = defaultFC7, defaultFC7IP

		self.BeBoard = QtBeBoard()
		self.BeBoard.setBoardName(firmwareName)
		self.BeBoard.setIPAddress(FirmwareList[firmwareName])
		self.BeBoard.setFPGAConfig(FPGAConfigList[firmwareName])

		self.master.FwDict[firmwareName] = self.BeBoard
		self.BeBoardWidget = SimpleBeBoardBox(self.BeBoard)
		#self.BeBoardWidget = BeBoardBox(self.BeBoard)  # not gona work, we dont want to use feature in expert gui
	
		LogFileName = "{0}/Gui/.{1}.log".format(os.environ.get("GUI_dir"),firmwareName)
		try:
			logFile  = open(LogFileName, "w")
			logFile.close()
		except:
			QMessageBox(None,"Error","Can not create log files: {}".format(LogFileName))
		
		FwStatusComment, FwStatusColor, FwStatusVerbose = self.master.getFwComment(firmwareName,LogFileName)
		if 'Connected' in FwStatusComment:
			self.FC7StatusValue.setPixmap(self.greenledpixmap)
		else:
			self.FC7StatusValue.setPixmap(self.redledpixmap)
		#self.FC7StatusValue.setText(FwStatusComment)
		#self.FC7StatusValue.setStyleSheet(FwStatusColor)
		self.FwModule = self.master.FwDict[firmwareName]
		
		self.StatusList.append([self.FC7NameLabel,self.FC7StatusValue])

		#self.ArduinoMonitor = ArduinoWidget()
		#self.ArduinoMonitor.stop.connect(self.GlobalStop)
		#self.ArduinoMonitor.enable()


		self.ArduinoGroup = ArduinoWidget()
		self.ArduinoGroup.stop.connect(self.master.GlobalStop)
		self.ArduinoGroup.enable()
		self.ArduinoGroup.setBaudRate(defaultSensorBaudRate)
		self.ArduinoGroup.frozeArduinoPanel()

		self.ArduinoMonitorLabel = QLabel()
		self.ArduinoMonitorValue = QLabel()
		self.ArduinoMonitorLabel.setText('Temperature and Humidity')
		
		if self.ArduinoGroup.ArduinoGoodStatus == True:
			self.ArduinoMonitorValue.setPixmap(self.greenledpixmap)
			
		else:
			self.ArduinoMonitorValue.setPixmap(self.redledpixmap)
			
		self.StatusList.append([self.ArduinoMonitorLabel,self.ArduinoMonitorValue])
		
		#note: the code at the following can be removed because the PLTA power check 
		#is done within the setup().

		#try:
			#self.Peltier = PeltierController(defaultPeltierPort, defaultPeltierBaud) #use setup()
			#self.Peltier.setTemperature(defaultPeltierSetTemp) #use setTemp()
			#self.Peltier.powerController(1)    #use controllerMonitoring()
			#the code at above are wrong need to fixed them


			#time.sleep(0.5)
			#self.PeltierPower = self.Peltier.checkPower()   #controllerMonitoring can check the poewr this will be removed in the future.
			#self.getPower() #old code dont use
			#print(self.PeltierPower + "self.PeltierPower debug")
			#print(self.setPowerStatus() + "self.setPowerStatus()")

		#except Exception as e:
			#print("Error while attempting to set Peltier", e)
			#self.PeltierPower = None


		self.PeltierMonitorLabel = QLabel()
		self.PeltierMonitorValue = QLabel()
		#self.PeltierMonitorValue.setText("Peltier Value")
		self.PeltierMonitorLabel.setText("Peltier Cooling")
		if int(self.powerStatusValue) == 1:
			self.PeltierMonitorValue.setPixmap(self.greenledpixmap)
		else:
			self.PeltierMonitorValue.setPixmap(self.redledpixmap)

#self.StatusList.append([self.PeltierMonitorLabel, self.PeltierMonitorValue])

		self.StatusLayout = QGridLayout()
		#for index, items in enumerate(self.StatusList):
		#	self.StatusLayout.addWidget(items[0], index, 1,  1, 1)
		#	self.StatusLayout.addWidget(items[1], index, 2,  1, 2)
		self.StatusLayout.addWidget(self.DBStatusLabel,0,1,1,1)
		self.StatusLayout.addWidget(self.DBStatusValue,0,2,1,1)
		self.StatusLayout.addWidget(self.HVPowerStatusLabel,0,3,1,1)
		self.StatusLayout.addWidget(self.HVPowerStatusValue,0,4,1,1)

		self.StatusLayout.addWidget(self.LVPowerStatusLabel,1,1,1,1)
		self.StatusLayout.addWidget(self.LVPowerStatusValue,1,2,1,1)
		self.StatusLayout.addWidget(self.FC7NameLabel,1,3,1,1)
		self.StatusLayout.addWidget(self.FC7StatusValue,1,4,1,1)

		self.StatusLayout.addWidget(self.ArduinoMonitorLabel,2,1,1,1)
		self.StatusLayout.addWidget(self.ArduinoMonitorValue,2,2,1,1)
		#self.StatusLayout.addWidget(self.ArduinoGroup.ArduinoMeasureValue)
		self.StatusLayout.addWidget(self.PeltierMonitorLabel, 2, 3, 1, 1)
		self.StatusLayout.addWidget(self.PeltierMonitorValue, 2, 4, 1, 1)
		self.StatusLayout.addWidget(self.RefreshButton,3 ,5, 1, 2)
		#self.StatusLayout.addWidget(self.RefreshButton,len(self.StatusList) ,1, 1, 1)


		ModuleEntryLayout.addWidget(self.BeBoardWidget)
		
		self.AppOption = QGroupBox()
		self.StartLayout = QHBoxLayout()
		self.TestGroup = QGroupBox()
		self.TestGroupLayout = QVBoxLayout()
		#self.TestGroup = QWidget()
		self.ProductionButton = QRadioButton("&Production Test")
		self.QuickButton = QRadioButton("&Quick Test")
		self.ProductionButton.setChecked(True)
		#self.QuickButton.setChecked(True)
		self.TestGroupLayout.addWidget(self.ProductionButton)
		self.TestGroupLayout.addWidget(self.QuickButton)
		self.TestGroup.setLayout(self.TestGroupLayout)
		#self.ProductionButton.move(20,20)
		#self.QuickButton.move(20,40)

		self.ExitButton = QPushButton("&Exit")
		self.ExitButton.clicked.connect(self.master.close)
		self.StopButton = QPushButton(self)
		Stopimage = QImage("icons/Stop_v2.png").scaled(QSize(80,80), Qt.KeepAspectRatio, Qt.SmoothTransformation)
		Stoppixmap = QPixmap.fromImage(Stopimage)
		StopIcon = QIcon(Stoppixmap)
		self.StopButton.setIcon(StopIcon)
		self.StopButton.setIconSize(QSize(80,80))
		self.StopButton.clicked.connect(self.abortTest)
		self.StopButton.setDisabled(True)
		#self.RunButton = QPushButton("&Run Tests")
		self.RunButton = QPushButton(self)
		Goimage = QImage("icons/gosign_v1.svg").scaled(QSize(80,80), Qt.KeepAspectRatio, Qt.SmoothTransformation)
		Gopixmap = QPixmap.fromImage(Goimage)
		RunIcon = QIcon(Gopixmap)
		self.RunButton.setIcon(RunIcon)
		self.RunButton.setIconSize(QSize(80,80))
		self.RunButton.clicked.connect(self.runNewTest)
		self.StartLayout.addStretch(1)
		self.StartLayout.addWidget(self.TestGroup)
		#self.StartLayout.addWidget(self.ExitButton)
		self.StartLayout.addWidget(self.StopButton)
		self.StartLayout.addWidget(self.RunButton)
		self.AppOption.setLayout(self.StartLayout)

		
		self.simplifiedStatusBox.setLayout(self.StatusLayout)
		self.ModuleEntryBox.setLayout(ModuleEntryLayout)
		#self.mainLayout.addWidget(self.welcomebox)
		self.mainLayout.addWidget(self.simplifiedStatusBox)
		self.mainLayout.addWidget(self.ModuleEntryBox)
		self.mainLayout.addWidget(self.AppOption)
		self.mainLayout.addWidget(self.LogoGroupBox)

	def runNewTest(self):
		for module in self.BeBoardWidget.getModules():
			if module.getSerialNumber() == "":
				QMessageBox.information(None,"Error","No valid serial number!", QMessageBox.Ok)
				return
			if module.getID() == "":
				QMessageBox.information(None,"Error","No valid ID!", QMessageBox.Ok)
				return
		
		self.firmwareDescription = self.BeBoardWidget.getFirmwareDescription() #debug: does this is being run? No!
		if self.FwModule.getModuleByIndex(0) == None:
			QMessageBox.information(None,"Error","No valid Module found!  If manually entering module number be sure to press 'Enter' on keyboard.", QMessageBox.Ok)
			return
		if self.ProductionButton.isChecked():
			self.info = [self.FwModule.getModuleByIndex(0).getOpticalGroupID(), "AllScan"]
		else:
			self.info = [self.FwModule.getModuleByIndex(0).getOpticalGroupID(), "QuickTest"]
			
		self.runFlag = True
		self.RunTest = QtRunWindow(self.master, self.info, self.firmwareDescription)
		self.LVpowersupply.setPoweringMode(defaultPowerMode)
		#self.LVpowersupply.setCompCurrent(compcurrent = 1.05) # Fixed for different chip
		self.LVpowersupply.setModuleType(defaultModuleType)
		self.LVpowersupply.TurnOn()
		#self.HVpowersupply.RampingUp(-60,-3)
		current = self.LVpowersupply.ReadCurrent()
		current = float(current) if current else 0.0
		voltage = self.LVpowersupply.ReadVoltage()
		voltage = float(voltage) if voltage else 0.0
		#print('Current = {0}'.format(current))
		self.RunButton.setDisabled(True)
		self.StopButton.setDisabled(False)

		self.RunTest.resetConfigTest()
		self.RunTest.initialTest()
		#self.RunTest.runTest()

	def abortTest(self):
		self.RunTest.abortTest()
		self.StopButton.setDisabled(True)
		self.RunButton.setDisabled(False)


	def checkDevices(self):
		statusString, colorString = checkDBConnection(self.connection)
		if 'offline' in statusString:
			self.DBStatusValue.setPixmap(self.redledpixmap)
		else:
			self.DBStatusValue.setPixmap(self.greenledpixmap)
		#self.DBStatusValue.setText(statusString)
		#self.DBStatusValue.setStyleSheet(colorString)

		#Selecting default HV
		self.HVpowersupply.setPowerModel(defaultHVModel[0])
		self.HVpowersupply.setInstrument(defaultUSBPortHV[0])
		statusString = self.HVpowersupply.getInfo()
		self.HVPowerStatusLabel.setText("HV status")
		if statusString != "No valid device" and statusString != None:
			#self.HVPowerStatusValue.setStyleSheet("color:green")
			self.HVPowerStatusValue.setPixmap(self.greenledpixmap)
		else:
			#self.HVPowerStatusValue.setStyleSheet("color:red")
			self.HVPowerStatusValue.setPixmap(self.redledpixmap)
		time.sleep(0.5)
		#Selecting default LV
		self.LVpowersupply.setPowerModel(defaultLVModel[0])
		self.LVpowersupply.setInstrument(defaultUSBPortLV[0])
		statusString = self.LVpowersupply.getInfo()
		self.LVPowerStatusLabel.setText("LV status")
		if statusString != "No valid device" and statusString != None:
			#self.LVPowerStatusValue.setStyleSheet("color:green")
			self.LVPowerStatusValue.setPixmap(self.greenledpixmap)
		else:
			#self.LVPowerStatusValue.setStyleSheet("color:red")
			self.LVPowerStatusValue.setPixmap(self.redledpixmap)

		firmwareName, fwAddress = defaultFC7, defaultFC7IP
	
		LogFileName = "{0}/Gui/.{1}.log".format(os.environ.get("GUI_dir"),firmwareName)
		try:
			logFile  = open(LogFileName, "w")
			logFile.close()
		except:
			QMessageBox(None,"Error","Can not create log files: {}".format(LogFileName))
		
		FwStatusComment, FwStatusColor, FwStatusVerbose = self.master.getFwComment(firmwareName,LogFileName)
		if 'Connected' in FwStatusComment:
			self.FC7StatusValue.setPixmap(self.greenledpixmap)
		else:
			self.FC7StatusValue.setPixmap(self.redledpixmap)

		
		#self.FC7StatusValue.setText(FwStatusComment)
		#self.FC7StatusValue.setStyleSheet(FwStatusColor)
		self.FwModule = self.master.FwDict[firmwareName]
		
		#self.StatusList.append([self.FC7NameLabel,self.FC7StatusValue])
		
		#Arduino stuff
		#self.ArduinoGroup = ArduinoWidget()
		self.ArduinoGroup.stop.connect(self.master.GlobalStop)
		self.ArduinoGroup.createArduino()
		self.ArduinoGroup.enable()
		self.ArduinoGroup.setBaudRate(defaultSensorBaudRate)
		self.ArduinoGroup.frozeArduinoPanel()

		#self.ArduinoMonitorLabel = QLabel()
		#self.ArduinoMonitorValue = QLabel()
		if self.ArduinoGroup.ArduinoGoodStatus == True:
			self.ArduinoMonitorValue.setPixmap(self.greenledpixmap)
		else:
			self.ArduinoMonitorValue.setPixmap(self.redledpixmap)

		#self.StatusList.append([self.ArduinoMonitorLabel,self.ArduinoMonitorValue])

		#for index, items in enumerate(self.StatusList):
		#	self.StatusLayout.addWidget(items[0], index, 1,  1, 1)
		#	self.StatusLayout.addWidget(items[1], index, 2,  1, 2)

		#self.StatusLayout.addWidget(self.RefreshButton,len(self.StatusList) ,1, 1, 1)



		######################################
		## Testin some things out (end) #######
		######################################	


