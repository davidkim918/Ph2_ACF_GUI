#this code is modified based on Ryan's PLTA cooling

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import *
from Gui.python.Peltier import *
import time
import os

class Peltier(QWidget):
    # Defining Signals that will be used
    buttonEnable = pyqtSignal()
    polaritySignal = pyqtSignal(list)
    tempReading = pyqtSignal(float)
    powerReading = pyqtSignal(int)
    setTempSignal = pyqtSignal(float)
    def __init__(self, dimension):
        super(Peltier, self).__init__()
        #self.setupUi()
        self.setup()
        self.setTemp()
        self.polarityToggle()
        self.powerToggle()
        time.sleep(120)
        #power toggle and then turn off the power with toggle

    """
    def setupUi(self):
        self.gridLayout = QtWidgets.QGridLayout(self)

        self.currentSetTemp = QtWidgets.QLabel("Current Set Temperature: ", self)
        self.setTempSignal.connect(lambda setTempValue: self.currentSetTemp.setText(f"Current Set Temp: {str(setTempValue)}"))
        self.gridLayout.addWidget(self.currentSetTemp, 3,2,1,1)

        self.startButton = QtWidgets.QPushButton("Start Peltier Controller", self)
        self.startButton.clicked.connect(self.setup)
        self.gridLayout.addWidget(self.startButton, 0,0,1,1)

        self.currentTempDisplay = QtWidgets.QLCDNumber(self)
        self.gridLayout.addWidget(self.currentTempDisplay, 3, 0, 1, 2)

        self.setTempButton = QtWidgets.QPushButton("Set Temperature", self)
        self.setTempButton.setEnabled(False)
        self.setTempButton.clicked.connect(self.setTemp)
        self.gridLayout.addWidget(self.setTempButton, 1, 1, 1, 1)

        self.setTempInput = QtWidgets.QDoubleSpinBox(self)
        self.setTempInput.setRange(-50,50)
        self.gridLayout.addWidget(self.setTempInput, 1, 0, 1, 1)

        self.currentTempLabel = QtWidgets.QLabel(self)
        self.gridLayout.addWidget(self.currentTempLabel, 2, 0, 1, 1)

        self.polarityButton = QtWidgets.QPushButton("Change Polarity", self)
        self.polarityButton.setEnabled(False)
        self.polarityButton.clicked.connect(self.polarityToggle)
        self.gridLayout.addWidget(self.polarityButton, 2, 1, 1, 1)

        self.powerStatus = QtWidgets.QLabel(self)
        self.powerStatusLabel = QtWidgets.QLabel("Power Status of Peltier: ", self)
        self.powerButton = QtWidgets.QPushButton("Peltier Power On/Off")
        self.powerButton.setEnabled(False)
        self.powerButton.clicked.connect(self.powerToggle)
        self.gridLayout.addWidget(self.powerButton, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.powerStatusLabel, 1, 2, 1, 1)

        self.image = QtGui.QPixmap()
        redledimage = QtGui.QImage(self.Ph2ACFDirectory + "/Gui/icons/led-red-on.png").scaled(QtCore.QSize(60,10), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.redledpixmap = QtGui.QPixmap.fromImage(redledimage)
        greenledimage = QtGui.QImage(self.Ph2ACFDirectory + "/Gui/icons/green-led-on.png" ).scaled(QtCore.QSize(60,10), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.greenledpixmap = QtGui.QPixmap.fromImage(greenledimage)
        self.powerStatus.setPixmap(self.redledpixmap) # The power status will initially always show that it's off, if it's actually on the status will be update in 0.5 seconds.
        self.gridLayout.addWidget(self.powerStatus, 1, 3, 1, 1)




        self.setLayout(self.gridLayout)
    
    """
    
    def setup(self):
        try:
            self.pelt = PeltierSignalGenerator()
            #self.buttonEnable.connect(self.enableButtons)
            self.polaritySignal.connect(self.setPolarityStatus)

            # These should emit signals
            self.pelt.sendCommand(self.pelt.createCommand('Set Type Define Write', ['0','0','0','0','0','0','0','0'])) # Allows set point to be set by computer software
            self.pelt.sendCommand(self.pelt.createCommand('Control Type Write', ['0','0','0','0','0','0','0','1'])) # Temperature should be PID controlled
            self.pelt.sendCommand(self.pelt.createCommand('Power On/Off Write' ,['0','0','0','0','0','0','0','0'])) # Turn off power to Peltier in case it is on at the start
            self.pelt.sendCommand(self.pelt.createCommand('Proportional Bandwidth Write', ['0','0','0','0','0','0', 'c', '8'])) # Set proportional bandwidth
            message, _= self.pelt.sendCommand(self.pelt.createCommand('Control Output Polarity Read', ['0','0','0','0','0','0','0','0']))

            #self.buttonEnable.emit()
            self.polaritySignal.emit(message)

            time.sleep(1) # Needed to avoid collision with temperature and power reading

            #Start temperature and power monitoring

            # Create QTimer that will call functions
            self.timer = QTimer()
            self.timer.timeout.connect(self.controllerMonitoring)
            self.tempReading.connect(lambda temp: self.currentTempDisplay.display(temp))
            self.powerReading.connect(lambda power: self.setPowerStatus(power))
            self.timer.start(500) # Perform monitoring functions every 500ms

        except Exception as e:
            print(e)
            print("Error while attempting to setup Peltier Controller: ", e)

    """
    def enableButtons(self):
        self.powerButton.setEnabled(True)
        self.polarityButton.setEnabled(True)
        self.setTempButton.setEnabled(True)
    """
    


    def setPowerStatus(self, power):
        if power == 1:
            self.powerStatus.setPixmap(self.greenledpixmap)
            self.powerStatusValue =1

        elif power == 0:
            self.powerStatus.setPixmap(self.redledpixmap)
            self.powerStatusValue =0
        else:
            print("Unkown power status")

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
            self.polarityButton.setText(self.polarityValue)
        elif polarity[8] == '1':
            self.polarityValue = 'HEAT WP2+ and WP1-'
            self.polarityButton.setText(self.polarityValue)
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
            message = self.convertSetTempValueToList(self.setTempInput.value())

            self.pelt.sendCommand(self.pelt.createCommand('Fixed Desired Control Setting Write', message))
            time.sleep(0.5) # Sleep to make sure controller has time to set temperature

            message , _ = self.pelt.sendCommand(self.pelt.createCommand('Fixed Desired Control Setting Read', ['0','0','0','0','0','0','0','0']))
            message = self.convertSetTempListToValue(message)

            self.setTempSignal.emit(message)

        except Exception as e:
            print("Could not set Temperature: " , e)
            self.currentSetTemp.setText("N/a")

    
    
    
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

# Shutdown the peltier if it is on and stop threads that are running
# Currently not implemented
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


    def getPower(self):
        try:
            self.power = self.controllerMonitoring()
        except Exception as e:
            self.powerTimer.stop()
            print("Could not check power due to error: " , e)









# Takes in a list
    def showTemp(self, message):
        try:
            temp = self.pelt.readTemperature()
            self.currentTempDisplay.display(temp)
        except Exception as e:
            self.timer.stop()
            print("Could not read temperature due to error: ", e)

    def setBandwidth(self):
        signalworker = signalWorker('Proportional Bandwidth Write', message)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Peltier(500)
    sys.exit(app.exec_())
