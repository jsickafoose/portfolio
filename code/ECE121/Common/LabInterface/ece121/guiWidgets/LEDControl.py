from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5

from ece121 import Protocol


widgetName = "LED Control"

class LEDControl(QWidget):

	def __init__(self, portInstance, parent=None):
		super(LEDControl, self).__init__(parent)

		self.portInstance = portInstance

		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)

		self.usedLayout.addWidget(QLabel("Hello Widget"))

		checkLayout = QHBoxLayout()

		self.usedLayout.addLayout(checkLayout)

		self.ledCheckButtons = list()
		for i in range(7, -1, -1):
			newCheck = QCheckBox("{}".format(i))
			# newCheck.setTristate(False)
			checkLayout.addWidget(newCheck)
			newCheck.clicked.connect(self.handleLEDOut)
			self.ledCheckButtons.append(newCheck)
		checkLayout.addStretch()

		# self.portInstance.requestLEDState()

		self.usedLayout.addStretch()
		return

	def setCheckBoxes(self, inPattern):
		# print(inPattern)
		for index, check in enumerate(self.ledCheckButtons):
			# print(check)
			# print(index)
			if inPattern & (1 << (7-index)):
				check.setCheckState(2)
			else:
				check.setCheckState(0)

	def getCheckBoxes(self):
		outPattern = 0
		for index, check in enumerate(self.ledCheckButtons):
			if check.checkState() == 2:
				outPattern |= (1 << (7-index))
		return outPattern

	def handleLEDIn(self, inBytes):
		self.setCheckBoxes(inBytes[1])
		return

	def handleLEDOut(self):
		ledPattern = self.getCheckBoxes()
		# print(ledPattern)
		messageOut = Protocol.MessageIDs.ID_LEDS_SET.value.to_bytes(1, byteorder='big')
		messageOut += ledPattern.to_bytes(1, byteorder='big')
		# print(messageOut)
		self.portInstance.sendRawMessage(messageOut)
		return
