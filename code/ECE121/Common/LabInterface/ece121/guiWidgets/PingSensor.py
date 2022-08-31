from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5
import struct

from ece121 import Protocol


widgetName = "Ping Sensor Reading"

class PingSensor(QWidget):
	signal = pyqtSignal(int)
	def __init__(self, portInstance, parent=None):
		super().__init__(parent)

		self.portInstance = portInstance

		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)

		# self.usedLayout.addWidget(QLabel("Hello Widget"))

		self.usedLayout.addWidget(QLabel("Current Distance"))
		self.distanceReading = QLabel()
		self.usedLayout.addWidget(self.distanceReading)
		self.signal.connect(self.updateGui)

		# self.angleReading = QLabel()
		# self.usedLayout.addWidget(self.angleReading)


		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_PING_DISTANCE, self.DistanceUpdates)

		# self.usedLayout.addSpacerItem(QSpacerItem())
		self.usedLayout.addStretch()
		return

	def DistanceUpdates(self, inBytes):
		# print(inBytes)\
		# print(inBytes[1:].hex())
		number = struct.unpack("!H", inBytes[1:])
		# print(number)
		self.signal.emit(number[0])
		return

	def updateGui(self, newNumber):
		# print('woo', newNumber)
		self.distanceReading.setText(str(newNumber))
		# self.angleReading.setText("{}".format((newNumber/16535)*360))
		return


