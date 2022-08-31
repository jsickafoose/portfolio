from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5
import random
import struct

from ece121 import Protocol


widgetName = "Lab 1 Application"

class Lab1Application(QWidget):

	def __init__(self, portInstance, parent=None):
		super(Lab1Application, self).__init__(parent)

		self.portInstance = portInstance

		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)


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

		compression = QHBoxLayout()
		self.askForLEDsButton = QPushButton("Request LED State")
		self.askForLEDsButton.clicked.connect(self.handleRequestLEDs)
		compression.addWidget(self.askForLEDsButton)
		compression.addWidget(QLabel("LED State: "))
		self.LEDStateLabel = QLabel("N/A")
		compression.addWidget(self.LEDStateLabel)
		compression.addStretch()
		self.usedLayout.addLayout(compression)
		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_LEDS_STATE, self.handleLEDIn)

		compression = QHBoxLayout()
		self.sendPingButton = QPushButton("Send Ping")
		self.sendPingButton.clicked.connect(self.sendPing)
		compression.addWidget(self.sendPingButton)
		compression.addWidget(QLabel("Sent Ping: "))
		self.sentPingLabel = QLabel()
		compression.addWidget(self.sentPingLabel)

		compression.addWidget(QLabel("\tReceived Pong: "))
		self.receivedPongLabel = QLabel()
		compression.addWidget(self.receivedPongLabel)

		self.successLabel = QLabel()
		compression.addWidget(self.successLabel)

		compression.addStretch()
		self.usedLayout.addLayout(compression)
		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_PONG, self.handlePong)

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
		payload = inBytes[1:]
		self.LEDStateLabel.setText("0X{}".format(payload.hex().upper()))
		return

	def handleLEDOut(self):
		ledPattern = self.getCheckBoxes()
		# print(ledPattern)
		messageOut = Protocol.MessageIDs.ID_LEDS_SET.value.to_bytes(1, byteorder='big')
		messageOut += ledPattern.to_bytes(1, byteorder='big')
		# print(messageOut)
		self.portInstance.sendRawMessage(messageOut)
		return

	def handleRequestLEDs(self):
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_LEDS_GET, b'')
		return

	def sendPing(self):
		pingValue = random.randint(0, 2**32-1)
		self.sentPingLabel.setText(str(pingValue))
		payload = struct.pack(">I", pingValue)
		# print(pingValue, payload.hex())
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_PING, payload)
		return

	def handlePong(self, inBytes):
		payload = inBytes[1:]
		pongValue = struct.unpack(">I", payload)[0]
		self.receivedPongLabel.setText(str(pongValue))
		if int(int(self.sentPingLabel.text())/2) == pongValue:
			self.successLabel.setText("\tSuccess")
		else:
			self.successLabel.setText("\tFailure")
		return
