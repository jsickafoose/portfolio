from sys import byteorder

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5
from functools import partial
from ece121 import Protocol
import struct
from . import FrequencyControl

widgetName = "ADC Readings and filtering"

lowPassCoefficients = [-54, -64, -82, -97, -93, -47, 66, 266, 562, 951, 1412, 1909, 2396, 2821, 3136, 3304, 3304, 3136,
							2821, 2396, 1909, 1412, 951, 562, 266, 66, -47, -93, -97, -82, -64, -54]
highPassCoefficients = [0, 0, 39, -91, 139, -129, 0, 271, -609, 832, -696, 0, 1297, -3011, 4755, -6059, 6542, -6059,
							4755, -3011, 1297, 0, -696, 832, -609, 271, 0, -129, 139, -91, 39, 0]
bandPassCoefficients = [73, -88, -90, 49, -74, 294, 569, -786, -781, 384, -514, 1899, 3608, -5354, -6787, 7595, 7595,
						-6787, -5354, 3608, 1899, -514, 384, -781, -786, 569, 294, -74, 49, -90, -88, 73]

class ADCReadings(QWidget):
	signal = pyqtSignal(int)
	adsignal = pyqtSignal(tuple)

	def __init__(self, portInstance, parent=None):
		super(ADCReadings, self).__init__(parent)

		self.portInstance = portInstance

		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)

		self.valueHistory = list()

		channelControlBox = QHBoxLayout()

		self.usedLayout.addLayout(channelControlBox)
		channelControlBox.addWidget(QLabel("Channel: "))

		self.channelSelect = QComboBox()
		self.channelSelect.addItems([str(i) for i in range(4)])
		channelControlBox.addWidget(self.channelSelect)

		self.changeChannelButton = QPushButton("Change Channel")
		channelControlBox.addWidget(self.changeChannelButton)
		self.changeChannelButton.clicked.connect(self.selectChannel)
		channelControlBox.addStretch()

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
		self.lowButton = QPushButton("Load Low Pass")
		filterBox.addWidget(self.lowButton)
		self.lowButton.clicked.connect(partial(self.SendFilterCoeffificients, lowPassCoefficients))

		# self.bandButton = QPushButton("Load Band Pass")
		# channelControlBox.addWidget(self.bandButton)
		# self.bandButton.clicked.connect(partial(self.SendFilterCoeffificients, bandPassCoefficients))
		#
		self.highButton = QPushButton("Load High Pass")
		filterBox.addWidget(self.highButton)
		self.highButton.clicked.connect(partial(self.SendFilterCoeffificients, highPassCoefficients))

		self.bandButton = QPushButton("Load Band Pass")
		filterBox.addWidget(self.bandButton)
		self.bandButton.clicked.connect(partial(self.SendFilterCoeffificients, bandPassCoefficients))

		filterBox.addStretch()
		self.usedLayout.addLayout(filterBox)

		for name, values in zip(["Low Pass", "High Pass", "Band Pass"], [lowPassCoefficients, highPassCoefficients, bandPassCoefficients]):
			compression = QHBoxLayout()
			compression.addWidget(QLabel(name))
			coeffs = QLineEdit()
			coeffs.setReadOnly(True)
			coeffs.setText("{"+", ".join([str(x) for x in values])+"}")
			compression.addWidget(coeffs)
			self.usedLayout.addLayout(compression)

		# self.ADValue = QLabel()
		# self.usedLayout.addWidget(self.ADValue)

		# self.signal.connect(self.updateGui)

		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_ADC_READING, self.newReadings)
		self.adsignal.connect(self.updateGui)
		# self.usedLayout.addSpacerItem(QSpacerItem())

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

	def updateGui(self, newReadings):
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


	def SendFilterCoeffificients(self, values):
		# pin = int(self.channelSelect.currentText())
		# fullPayload = [pin]
		fullPayload = values
		fullPayload = struct.pack("!"+"h"*len(fullPayload), *fullPayload)
		# print(fullPayload)
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_ADC_FILTER_VALUES, fullPayload)
		# print(values)
		return

	def selectChannel(self):
		pin = int(self.channelSelect.currentText())
		# print(pin)
		fullPayload = struct.pack("!B", pin)
		# print(fullPayload)
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_ADC_SELECT_CHANNEL, fullPayload)
		self.valueHistory.clear()
		return