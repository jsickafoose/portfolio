from sys import byteorder

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5
from functools import partial
from ece121 import Protocol
import struct


widgetName = "RC Servo Control"

class RCServo(QWidget):
	signal = pyqtSignal(int)
	def __init__(self, portInstance, parent=None):
		super(RCServo, self).__init__(parent)

		self.portInstance = portInstance

		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)

		# self.usedLayout.addWidget(QLabel("Hello Widget"))

		self.centerTicks = 1500
		self.currentTick = self.centerTicks
		self.minTicks = 600
		self.maxTicks = 2400


		self.usedLayout.addWidget(QLabel("Current RC ticks"))
		self.RCValue = QLabel()
		self.usedLayout.addWidget(self.RCValue)
		self.RCValue.setText(str(self.currentTick))
		# self.signal.connect(self.updateGui)

		self.ServoDisplay = QSlider(Qt.Horizontal)
		self.ServoDisplay.setValue(self.currentTick)
		self.ServoDisplay.setRange(self.minTicks, self.maxTicks)
		self.ServoDisplay.setValue(self.centerTicks)
		self.ServoDisplay.setTickPosition(2)
		self.ServoDisplay.setTickInterval(25)
		self.ServoDisplay.setSingleStep(25)
		# self.SpeedDisplay.setTracking(False)
		self.ServoDisplay.valueChanged.connect(self.sliderChanged)

		self.usedLayout.addWidget(self.ServoDisplay)

		buttonLayout = QHBoxLayout()
		self.usedLayout.addLayout(buttonLayout)

		fullRev = QPushButton("+")
		buttonLayout.addWidget(fullRev)
		fullRev.clicked.connect(partial(self.ServoDisplay.setSliderPosition, self.minTicks))

		fullRev = QPushButton("0")
		buttonLayout.addWidget(fullRev)
		fullRev.clicked.connect(partial(self.ServoDisplay.setSliderPosition, self.centerTicks))

		fullRev = QPushButton("+")
		buttonLayout.addWidget(fullRev)
		fullRev.clicked.connect(partial(self.ServoDisplay.setSliderPosition, self.maxTicks))

		self.usedLayout.addWidget(QLabel("Servo Response"))
		self.ServoResponse = QLabel()
		self.usedLayout.addWidget(self.ServoResponse)
		self.ServoResponse.setText(str(0))
		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_SERVO_RESPONSE, self.servoResponded)


		# self.angleDisplay = QDial()
		# self.angleDisplay.setWrapping(True)
		# self.angleDisplay.setRange(0,360)

		# self.usedLayout.addWidget(self.angleDisplay)


		# self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_ROTARY_ANGLE, self.RotaryUpdates)

		# self.usedLayout.addSpacerItem(QSpacerItem())
		self.usedLayout.addStretch()
		return

	def sliderChanged(self, newValue):


		if newValue != self.currentTick:
			if abs(newValue - self.currentTick) > 5:
				# print(newValue)
				self.currentTick = newValue
				self.RCValue.setText(str(self.currentTick))
				message = Protocol.MessageIDs.ID_COMMAND_SERVO_PULSE.value.to_bytes(1, byteorder='big')
				message += self.currentTick.to_bytes(4, byteorder='big', signed=True)
				self.portInstance.sendRawMessage(message)

		return

	def servoResponded(self, rawBytes):
		value = struct.unpack("!i", rawBytes[1:])[0]
		self.ServoResponse.setText(str(value))
		return

