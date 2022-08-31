from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5
import struct
from functools import partial
import datetime
from ece121 import Protocol
from . import ADCReadings
from . import FrequencyControl

widgetName = "Lab 3 Application"


class Lab3Application(QWidget):
	signal = pyqtSignal(tuple)
	adsignal = pyqtSignal(tuple)
	modeSignal = pyqtSignal(tuple)
	statusSignal = pyqtSignal(str)

	def __init__(self, portInstance, parent=None):
		super(Lab3Application, self).__init__(parent)

		self.portInstance = portInstance
		self.valueHistory = list()

		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)

		compression = QHBoxLayout()
		self.usedLayout.addLayout(compression)
		compression.addWidget(QLabel("Channel in Use: "))
		self.usedChannel = QLabel("N/A")
		compression.addWidget(self.usedChannel)
		compression.addStretch()

		compression = QHBoxLayout()
		self.usedLayout.addLayout(compression)
		compression.addWidget(QLabel("Filter in Use: "))
		self.usedFilter = QLabel("N/A")
		compression.addWidget(self.usedFilter)
		compression.addStretch()

		readingsBox = QHBoxLayout()
		readingsGrid = QGridLayout()
		readingsBox.addLayout(readingsGrid)
		readingsBox.addStretch()
		self.usedLayout.addLayout(readingsBox)
		readingsGrid.addWidget(QLabel("Raw Reading"), 0, 1, alignment=Qt.AlignCenter)
		readingsGrid.addWidget(QLabel("Filtered Reading"), 0, 2, alignment=Qt.AlignCenter)
		readingsGrid.addWidget(QLabel("Absolute Value"), 0, 3, alignment=Qt.AlignCenter)
		readingsGrid.addWidget(QLabel("Peak-To-Peak"), 0, 4, alignment=Qt.AlignCenter)
		readingsGrid.addWidget(QLabel("Min Value "), 0, 5, alignment=Qt.AlignCenter)
		readingsGrid.addWidget(QLabel("Max Value"), 0, 6, alignment=Qt.AlignCenter)
		self.ADValues = list()
		self.ADValues.append(QLabel("0"))
		readingsGrid.addWidget(self.ADValues[-1], 1, 1, alignment=Qt.AlignCenter)
		self.ADValues.append(QLabel("0"))
		readingsGrid.addWidget(self.ADValues[-1], 1, 2, alignment=Qt.AlignCenter)
		self.ADValues.append(QLabel("0"))
		readingsGrid.addWidget(self.ADValues[-1], 1, 3, alignment=Qt.AlignCenter)
		self.ADValues.append(QLabel("0"))
		readingsGrid.addWidget(self.ADValues[-1], 1, 4, alignment=Qt.AlignCenter)
		self.ADValues.append(QLabel("0"))
		readingsGrid.addWidget(self.ADValues[-1], 1, 5, alignment=Qt.AlignCenter)
		self.ADValues.append(QLabel("0"))
		readingsGrid.addWidget(self.ADValues[-1], 1, 6, alignment=Qt.AlignCenter)

		filterBox = QHBoxLayout()
		self.lowButton = QPushButton("Send Low Pass")
		filterBox.addWidget(self.lowButton)
		self.lowButton.clicked.connect(partial(self.SendFilterCoeffificients, ADCReadings.lowPassCoefficients))
		self.highButton = QPushButton("Send High Pass")
		filterBox.addWidget(self.highButton)
		self.highButton.clicked.connect(partial(self.SendFilterCoeffificients, ADCReadings.highPassCoefficients))
		filterBox.addStretch()
		self.usedLayout.addLayout(filterBox)

		compression = QHBoxLayout()
		compression.addWidget(QLabel("Status: "))
		self.status = QLabel("N/A")
		compression.addWidget(self.status)
		compression.addStretch()
		self.usedLayout.addLayout(compression)

		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_ADC_READING, self.newReadings)
		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_LAB3_CHANNEL_FILTER, self.modeChange)
		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_ADC_FILTER_VALUES_RESP, self.filterLoad)

		self.adsignal.connect(self.updateReadings)
		self.modeSignal.connect(self.modeChangeGui)
		self.statusSignal.connect(self.updateStatus)



		self.freqControl = FrequencyControl.FrequencyControl(self.portInstance)
		self.usedLayout.addWidget(self.freqControl)

		self.usedLayout.addStretch()
		return


	def newReadings(self, newValue):
		payload = newValue[1:]
		# newReading = int.from_bytes(newValue[1:], byteorder='little')
		values = struct.unpack("!hh", payload)
		# print(values)
		self.adsignal.emit(values)
		return

	def updateReadings(self, newReadings):
		# print(newReadings)
		self.valueHistory.append(newReadings[1])
		if len(self.valueHistory) > 100:
			self.valueHistory.pop(0)
		# print(len(self.valueHistory))
		for reading, label in zip(newReadings, self.ADValues):
			label.setText(str(reading))
		# self.ADValue.setText("Reading: {}".format(newReading))
		self.ADValues[2].setText(str(abs(self.valueHistory[-1])))
		self.ADValues[3].setText(str(max(self.valueHistory) - min(self.valueHistory)))
		self.ADValues[4].setText(str(min(self.valueHistory)))
		self.ADValues[5].setText(str(max(self.valueHistory)))

		return


	def modeChange(self, newPacket):
		payload = newPacket[1:]
		rawModes = struct.unpack("!b", payload)[0]
		self.modeSignal.emit(((rawModes >> 4) & 0xF, rawModes & 0xF))
		self.statusSignal.emit("Mode Change occurred")
		return

	def modeChangeGui(self, newModes):
		self.usedChannel.setText(str(newModes[0]))
		self.usedFilter.setText(str(newModes[1]))
		return

	def SendFilterCoeffificients(self, values):
		# pin = int(self.channelSelect.currentText())
		# fullPayload = [pin]
		fullPayload = values
		fullPayload = struct.pack("!"+"h"*len(fullPayload), *fullPayload)
		# print(fullPayload)
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_ADC_FILTER_VALUES, fullPayload)
		# print(values)
		return

	def filterLoad(self, newBytes):
		self.statusSignal.emit("New Filter Stored to Memory")
		return

	def updateStatus(self, newStatus):
		newStatus += ' at ' + str(datetime.datetime.now())
		self.status.setText(newStatus)
		return