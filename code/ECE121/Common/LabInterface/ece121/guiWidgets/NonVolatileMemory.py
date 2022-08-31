from builtins import int

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5
from functools import partial
from ece121 import Protocol

import random
import struct

minAddress = 0
maxAddress = 100000
widgetName = "Non Volatile Memory"
titleFontSize = 20
pageSize = 64
class NonVolatileMemory(QWidget):
	signal = pyqtSignal(int)
	def __init__(self, portInstance, parent=None):
		super(NonVolatileMemory, self).__init__(parent)

		self.portInstance = portInstance

		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)

		sectionLabel = QLabel("Byte Mode")

		currentFont = sectionLabel.font()
		currentFont.setPointSize(titleFontSize)
		sectionLabel.setFont(currentFont)
		self.usedLayout.addWidget(sectionLabel)

		addressBox = QHBoxLayout()
		self.usedLayout.addLayout(addressBox)

		addressBox.addWidget(QLabel("Address: "))

		self.address = QLineEdit(str(0))
		self.address.setValidator(QIntValidator(minAddress, maxAddress))
		addressBox.addWidget(self.address)
		randomAddress = QPushButton("Randomize Address")
		randomAddress.clicked.connect(self.createNewAddress)
		addressBox.addWidget(randomAddress)
		addressBox.addStretch()

		writeBox = QHBoxLayout()
		self.usedLayout.addLayout(writeBox)
		self.writeButton = QPushButton("Write Address")
		self.writeButton.clicked.connect(self.startWrite)
		writeBox.addWidget(self.writeButton)
		writeBox.addWidget(QLabel("Value: "))
		self.writeValue = QLineEdit(str(0))
		self.writeValue.setValidator(QIntValidator(0, 255))
		writeBox.addWidget(self.writeValue)

		randomValue = QPushButton("Set Random Value")
		randomValue.clicked.connect(self.setRandomValue)
		writeBox.addWidget(randomValue)

		writeBox.addStretch()

		readBox = QHBoxLayout()
		self.usedLayout.addLayout(readBox)
		self.readButton = QPushButton("Read Address")
		self.readButton.clicked.connect(self.startRead)
		readBox.addWidget(self.readButton)
		readBox.addWidget(QLabel("Value: "))
		self.readValue = QLabel("N/A")
		readBox.addWidget(self.readValue)
		readBox.addStretch()

		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_NVM_READ_BYTE_RESP, self.respToRead)
		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_NVM_WRITE_BYTE_ACK, self. respToWrite)



		line = QFrame()
		line.setFrameShape(QFrame.HLine)
		line.setFrameShadow(QFrame.Sunken)
		self.usedLayout.addWidget(line)

		sectionLabel = QLabel("Page Mode")

		currentFont = sectionLabel.font()
		currentFont.setPointSize(titleFontSize)
		sectionLabel.setFont(currentFont)
		self.usedLayout.addWidget(sectionLabel)


		addressBox = QHBoxLayout()
		self.usedLayout.addLayout(addressBox)

		addressBox.addWidget(QLabel("Page Address: "))

		self.pageAddress = QLineEdit(str(0))
		self.pageAddress.setValidator(QIntValidator(int(minAddress/pageSize), int(maxAddress/pageSize)))
		addressBox.addWidget(self.pageAddress)
		randomPageAddress = QPushButton("Randomize Address")
		randomPageAddress.clicked.connect(self.createNewPageAddress)
		addressBox.addWidget(randomPageAddress)
		addressBox.addStretch()

		writeBox = QHBoxLayout()
		self.usedLayout.addLayout(writeBox)
		self.writePageButton = QPushButton("Write Page")
		self.writePageButton.clicked.connect(self.startPageWrite)
		writeBox.addWidget(self.writePageButton)
		writeBox.addWidget(QLabel("Value: "))
		self.pageWriteValue = QLineEdit("0X{:0{}X}".format(0x0, int(pageSize*2)))
		self.pageWriteValue.setDisabled(True)
		# self.writeValue.setValidator(QIntValidator(0, 255))
		writeBox.addWidget(self.pageWriteValue)

		pageRandomValue = QPushButton("Set Random Value")
		pageRandomValue.clicked.connect(self.createPageValue)
		writeBox.addWidget(pageRandomValue)
		writeBox.addStretch()

		readBox = QHBoxLayout()
		self.usedLayout.addLayout(readBox)
		self.readPageButton = QPushButton("Read Page")
		self.readPageButton.clicked.connect(self.startPageRead)
		readBox.addWidget(self.readPageButton)
		readBox.addWidget(QLabel("Value: "))
		self.readPageValue = QLabel("N/A")
		readBox.addWidget(self.readPageValue)
		readBox.addStretch()

		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_NVM_READ_PAGE_RESP, self.respToPageRead)


		line = QFrame()
		line.setFrameShape(QFrame.HLine)
		line.setFrameShadow(QFrame.Sunken)
		self.usedLayout.addWidget(line)

		statusBox = QHBoxLayout()
		self.usedLayout.addLayout(statusBox)
		statusBox.addWidget(QLabel("Status: "))
		self.statusText = QLabel("None")
		statusBox.addWidget(self.statusText)
		statusBox.addStretch()



		self.usedLayout.addStretch()
		return

	def createNewAddress(self):
		newAddress = random.randint(minAddress, maxAddress)
		self.address.setText(str(newAddress))
		return

	def createNewPageAddress(self):
		newAddress = random.randint(int(minAddress/pageSize), int(maxAddress/pageSize))
		self.pageAddress.setText(str(newAddress))
		return

	def createPageValue(self):
		newPageValue = random.randint(0, 2**(pageSize*8))
		self.pageWriteValue.setText("0X{:0{}X}".format(newPageValue, int(pageSize*2)))
		return

	def startWrite(self):
		# print("Write here")
		addressToWrite = int(max(0, min(maxAddress, int(self.address.text()))))
		valuetoWrite = int(max(0, min(255, int(self.writeValue.text()))))
		payload = struct.pack(">IB", addressToWrite, valuetoWrite)
		# print(payload)
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_NVM_WRITE_BYTE, payload)
		self.statusText.setText("Writing {} to address {}".format(valuetoWrite, addressToWrite))
		# self.setDisabled(True)
		return

	def startPageWrite(self):
		# print("Write here")

		addressToWrite = int(max(0, min(maxAddress/64, int(self.pageAddress.text()))))
		# addressToWrite = int(self.pageAddress.text())
		print(addressToWrite)
		valuetoWrite = int(self.pageWriteValue.text()[2:], 16)
		print(valuetoWrite)
		payload = bytearray()
		# for value in [(((0xff << i*8) & valuetoWrite)>> i*8) for i in range(64)]:
		# 	payload += bytes(value)
		payload = struct.pack("B"*64, *reversed([(((0xff << i*8) & valuetoWrite)>> i*8) for i in range(64)]))
		# print(payload.hex())
		payload = struct.pack("!I", addressToWrite)+payload
		# print(payload)
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_NVM_WRITE_PAGE, payload)
		self.statusText.setText("Writing {} to address {}".format(valuetoWrite, addressToWrite))
		# self.setDisabled(True)
		return

	def startRead(self):
		# print("Read here")
		addressToRead = int(max(0, min(maxAddress, int(self.address.text()))))
		# print(addressToRead)
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_NVM_READ_BYTE, struct.pack(">I", addressToRead))
		# self.setDisabled(True)
		self.statusText.setText("Reading data from address {}".format(addressToRead))
		return

	def startPageRead(self):
		# print("Read here")
		addressToRead = int(max(0, min(maxAddress/64, int(self.pageAddress.text()))))
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_NVM_READ_PAGE, struct.pack(">I", addressToRead))
		# self.setDisabled(True)
		self.statusText.setText("Reading data from address {}".format(addressToRead))
		return


	def respToRead(self, newBytes):
		payload = newBytes[1:]
		value = struct.unpack(">B", payload)[0]
		# self.setDisabled(False)
		self.statusText.setText("{} was read from memory".format(value))
		self.readValue.setText(str(value))
		return

	def respToPageRead(self, newBytes):
		payload = newBytes[1:]
		payload = '0X'+str(payload.hex()).upper()
		# value = struct.unpack("<B", payload)[0]
		# self.setDisabled(False)
		self.statusText.setText("{} was read from memory".format(payload))
		self.readPageValue.setText(payload)
		return

	def respToWrite(self, inBytes):
		# print(inBytes)
		self.statusText.setText("Wrote to memory".format())
		# self.setDisabled(False)
		return

	def setRandomValue(self):
		self.writeValue.setText(str(random.randint(0,255)))