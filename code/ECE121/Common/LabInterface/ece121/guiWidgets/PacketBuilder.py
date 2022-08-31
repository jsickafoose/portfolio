from builtins import int

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5
from functools import partial
from ece121 import Protocol

import struct
from collections import OrderedDict
import random

widgetName = "Packet Builder"
payloadTypes = OrderedDict({"char": 'b',
							"unsigned char": 'B',
							"short": 'h',
							"unsigned short": 'H',
							"int": 'i',
						   	"unsigned int": 'I'})

maxPacketLength = 8

randomMode = False

class PacketBuilder(QWidget):
	intsignal = pyqtSignal(int)
	def __init__(self, portInstance, parent=None):
		super(PacketBuilder, self).__init__(parent)

		self.portInstance = portInstance

		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)


		self.fullMessage = None
		self.payload = None

		curLine = QHBoxLayout()
		self.usedLayout.addLayout(curLine)
		curLine.addWidget(QLabel("Choose Packet"))
		self.PacketSelection = QComboBox()
		curLine.addWidget(self.PacketSelection)
		self.PacketSelection.addItems([x.name for x in Protocol.MessageIDs if "INVALID" not in x.name])
		self.PacketSelection.setCurrentIndex(1)
		curLine.addStretch()

		curLine = QHBoxLayout()
		self.usedLayout.addLayout(curLine)
		curLine.addWidget(QLabel("Items in Payload"))
		self.PacketItemCount = QComboBox()

		curLine.addWidget(self.PacketItemCount)
		self.PacketItemCount.addItems([str(x) for x in range(9)])
		if randomMode:
			self.PacketItemCount.setCurrentIndex(random.randint(0, self.PacketItemCount.count()-1))
		self.PacketItemCount.update()
		curLine.addStretch()

		# the ugly thing we now add is a set of vboxes each with a text field and a combobox
		payloadTypeSelectionList = list()
		Compression = QHBoxLayout()
		self.payloadArray = list()
		for i in range(maxPacketLength):
			self.payloadArray.append(QVBoxLayout())
			self.payloadArray[-1].addWidget(QLabel("Item {}".format(i+1)))
			ptype = QComboBox()
			ptype.addItems(payloadTypes.keys())
			if randomMode:
				ptype.setCurrentIndex(random.randint(0, len(payloadTypes)-1))
			self.payloadArray[-1].addWidget(ptype)
			payloadvalue = QLineEdit()
			if randomMode:
				payloadvalue.setText(str(random.randint(-100000, 100000))) # basically outside the range of chars and shorts
			else:
				payloadvalue.setText(str(0))
			payloadvalue.setValidator(QIntValidator())
			self.payloadArray[-1].addWidget(payloadvalue)
			Compression.addLayout(self.payloadArray[-1])

		self.handlepacketLengthUpdate()
		self.usedLayout.addLayout(Compression)

		# as soon as the rest of this part of the gui is instantiated we can add the message
		self.PacketItemCount.currentIndexChanged.connect(self.handlepacketLengthUpdate)
		# self.PacketItemCount.setCurrentIndex(1)

		line = QFrame()
		line.setFrameShape(QFrame.HLine)
		line.setFrameShadow(QFrame.Sunken)
		self.usedLayout.addWidget(line)

		Compression = QHBoxLayout()

		packetBreakUp = QGridLayout()
		Compression.addLayout(packetBreakUp)
		Compression.addStretch()

		header = QVBoxLayout()
		header.addWidget(QLabel("Header"))
		header.addWidget(QLabel("0X{:X}".format(int.from_bytes(Protocol.HEADER, byteorder='little'))))
		packetBreakUp.addLayout(header, 0, 0)

		length = QVBoxLayout()
		length.addWidget(QLabel("Length"))
		self.lengthLabel = QLabel("1")
		length.addWidget(self.lengthLabel)
		packetBreakUp.addLayout(length, 0, 1)

		payload = QVBoxLayout()
		payloadText = QLabel("Payload")
		payloadText.setAlignment(Qt.AlignCenter)
		payload.addWidget(payloadText)
		self.payloadLabel = QLabel("N/A")
		self.payloadLabel.setAlignment(Qt.AlignCenter)
		self.payloadLabel.setMinimumWidth(200)
		payload.addWidget(self.payloadLabel)
		packetBreakUp.addLayout(payload, 0, 2)

		footer = QVBoxLayout()
		footer.addWidget(QLabel("Tail"))
		footer.addWidget(QLabel("0X{:X}".format(int.from_bytes(Protocol.TAIL, byteorder='little'))))
		packetBreakUp.addLayout(footer, 0, 3)

		checksum = QVBoxLayout()
		checksum.addWidget(QLabel("Checksum"))
		self.checksumLabel = QLabel("0")
		self.checksumLabel.setAlignment(Qt.AlignCenter)
		checksum.addWidget(self.checksumLabel)
		packetBreakUp.addLayout(checksum, 0, 4)

		ender = QVBoxLayout()
		ender.addWidget(QLabel("Ending"))
		ender.addWidget(QLabel(r"0X{:02X}{:02X}".format(ord('\r'),ord('\n'))))
		# packetBreakUp.addLayout(header, 0, 0)
		packetBreakUp.addLayout(ender, 0, 5)

		self.usedLayout.addLayout(Compression)

		line = QFrame()
		line.setFrameShape(QFrame.HLine)
		line.setFrameShadow(QFrame.Sunken)
		self.usedLayout.addWidget(line)
		Compression = QHBoxLayout()

		self.usedLayout.addLayout(Compression)
		Compression.addWidget(QLabel("Full Packet"))
		self.fullPacketLabel = QLineEdit()
		self.fullPacketLabel.setReadOnly(True)
		self.fullPacketLabel.setText("Hello World")
		Compression.addWidget(self.fullPacketLabel)

		Compression = QHBoxLayout()

		self.usedLayout.addLayout(Compression)
		Compression.addWidget(QLabel("C Array"))
		self.cArrayExport = QLineEdit()
		self.cArrayExport.setReadOnly(True)
		self.cArrayExport.setText("Hello World")
		Compression.addWidget(self.cArrayExport)

		Compression = QHBoxLayout()
		self.usedLayout.addLayout(Compression)

		self.buildPacketButton = QPushButton("Build Packet")
		self.buildPacketButton.clicked.connect(self.BuildPacket)
		Compression.addWidget(self.buildPacketButton)

		self.sendPacketButton = QPushButton("Build and Send Packet")
		self.sendPacketButton.clicked.connect(self.sendPacket)
		Compression.addWidget(self.sendPacketButton)

		self.usedLayout.addStretch()



		self.BuildPacket()

		return

	def BuildPacket(self):
		"""actually build the packet here and update all the outputs"""

		self.fullMessage = Protocol.HEADER

		# we need to build the payload first to get the length

		payload = struct.pack(">B", Protocol.MessageIDs[self.PacketSelection.currentText()].value)

		numWanted = self.PacketItemCount.currentIndex()
		for arrayIndex in range(numWanted):
			variableType = self.payloadArray[arrayIndex].itemAt(1).widget().currentText()
			variableFormat = payloadTypes[variableType]
			variableSize = struct.calcsize(variableFormat)
			valueToPack = int(self.payloadArray[arrayIndex].itemAt(2).widget().text())
			# first step is to force the number positive if unsigned
			if 'unsigned' in variableType:
				valueToPack = abs(valueToPack)
				valueToPack = min(valueToPack, 2**(variableSize*8)-1)
			else:
				valueToPack = max(min(valueToPack, 2**(variableSize*8-1)-1), -2**(variableSize*8-1))
			payload += struct.pack(">"+variableFormat, valueToPack)
			self.payloadArray[arrayIndex].itemAt(2).widget().setText(str(valueToPack))

		packetLength = struct.pack(">B", len(payload))
		packetCheckSum = struct.pack(">B", self.portInstance.calcChecksum(payload))

		# print(payload.hex(), packetLength, packetCheckSum)

		self.fullMessage += packetLength + payload + Protocol.TAIL + packetCheckSum + b'\r\n'
		self.payload = payload

		self.lengthLabel.setText("0X{}".format(packetLength.hex().upper()))

		self.payloadLabel.setText("0X{}".format(payload.hex().upper()))

		self.checksumLabel.setText("0X{}".format(packetCheckSum.hex().upper()))

		self.fullPacketLabel.setText("0X{}".format(self.fullMessage.hex().upper()))

		self.cArrayExport.setText("{"+", ".join([str(x) for x in self.fullMessage])+"}")

		# print(fullMessage)

		return

	def sendPacket(self):
		self.BuildPacket()
		if self.payload is not None:
			self.portInstance.sendRawMessage(self.payload)
		return


	def handlepacketLengthUpdate(self):
		numWanted = self.PacketItemCount.currentIndex()
		# get rid of all of them and then add back the ones we want
		for payloaditem in self.payloadArray:
			for i in range(payloaditem.count()):
				hmm = payloaditem.itemAt(i).widget()
				hmm.setDisabled(True)

		for arrayIndex in range(numWanted):
			# print('huh', arrayIndex)
			for i in range(self.payloadArray[arrayIndex].count()):
				hmm = self.payloadArray[arrayIndex].itemAt(i).widget()
				hmm.setDisabled(False)
		# print(numWanted)
		return