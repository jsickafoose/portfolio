from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5
from functools import partial
from ece121 import Protocol
import struct


widgetName = "Frequency Generation"

presetFrequencies = [25, 125, 300, 450]

class FrequencyControl(QWidget):
	signal = pyqtSignal(int)
	feedbackSignal = pyqtSignal(tuple)
	def __init__(self, portInstance, parent=None):
		super().__init__(parent)

		self.portInstance = portInstance

		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)

		controlBox = QHBoxLayout()
		self.usedLayout.addLayout(controlBox)
		controlBox.addWidget(QLabel("Generator Control"))

		genOn = QPushButton("On")
		genOn.clicked.connect(partial(self.sendPowerMessage, 1))
		genOff = QPushButton("Off")
		genOff.clicked.connect(partial(self.sendPowerMessage, 0))

		controlBox.addWidget(genOn)
		controlBox.addWidget(genOff)

		controlBox.addStretch()

		presetBox = QHBoxLayout()
		self.usedLayout.addLayout(presetBox)
		presetBox.addWidget(QLabel("Preset Frequencies"))
		for freqWanted in presetFrequencies:
			newButton = QPushButton("{}Hz".format(freqWanted))
			newButton.clicked.connect(partial(self.sendFrequencyMessage, freqWanted))
			presetBox.addWidget(newButton)

		presetBox.addStretch()

		arbBox = QHBoxLayout()
		self.usedLayout.addLayout(arbBox)

		arbBox.addWidget(QLabel("Arbitrary Frequency"))

		self.arbFreqInput = QLineEdit()
		arbBox.addWidget(self.arbFreqInput)

		newValidator = QIntValidator()
		newValidator.setRange(0, 20000)
		self.arbFreqInput.setValidator(newValidator)
		self.arbFreqInput.setText(str(1))

		arbSendButton = QPushButton("Set Frequency")
		arbSendButton.clicked.connect(self.sendArbFreq)
		arbBox.addWidget(arbSendButton)


		arbBox.addStretch()

		self.statusMessage = QLabel("Init")
		self.usedLayout.addWidget(self.statusMessage)


	def sendPowerMessage(self, state):
		if state == 0:
			self.statusMessage.setText("Frequency Generator Turned Off")
		else:
			self.statusMessage.setText("Frequency Generator Turned On")
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_LAB3_FREQUENCY_ONOFF, struct.pack("b", state))
		return

	def sendFrequencyMessage(self, newFrequency):
		self.statusMessage.setText("Frequency Generator set to {}Hz".format(newFrequency))
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_LAB3_SET_FREQUENCY, struct.pack("!H", newFrequency))
		return

	def sendArbFreq(self):
		self.sendFrequencyMessage(int(self.arbFreqInput.text()))
		return