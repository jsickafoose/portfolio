from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5
import struct

from ece121 import Protocol


widgetName = "Rotary Encoder Reading"

class RotaryEncoder(QWidget):
	signal = pyqtSignal(int)
	def __init__(self, portInstance, parent=None):
		super(RotaryEncoder, self).__init__(parent)

		self.portInstance = portInstance

		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)

		# self.usedLayout.addWidget(QLabel("Hello Widget"))

		self.usedLayout.addWidget(QLabel("Current Rotary Reading"))
		self.rotaryReading = QLabel()
		self.usedLayout.addWidget(self.rotaryReading)
		self.signal.connect(self.updateGui)

		# self.angleReading = QLabel()
		# self.usedLayout.addWidget(self.angleReading)

		self.angleDisplay = QDial()
		self.angleDisplay.setNotchesVisible(True)
		self.angleDisplay.setWrapping(True)
		self.angleDisplay.setRange(0,360)

		self.usedLayout.addWidget(self.angleDisplay)


		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_ROTARY_ANGLE, self.RotaryUpdates)

		# self.usedLayout.addSpacerItem(QSpacerItem())
		self.usedLayout.addStretch()
		return

	def RotaryUpdates(self, inBytes):
		# print(inBytes)\
		# print(inBytes[1:].hex())
		number = struct.unpack("!H", inBytes[1:])
		# print(number)
		self.signal.emit(number[0])
		return

	def updateGui(self, newNumber):
		# print('woo', newNumber)
		self.rotaryReading.setText(str(newNumber))
		# self.angleReading.setText("{}".format((newNumber/16535)*360))
		self.angleDisplay.setValue(int((newNumber/16535)*360))
		return


