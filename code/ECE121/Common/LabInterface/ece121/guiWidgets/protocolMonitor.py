from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5
from ece121 import Protocol
import datetime
import queue

widgetName = "Protocol Monitor"


class protocolMonitor(QWidget):
	inStrSignal = pyqtSignal(str)
	outStrSignal = pyqtSignal(str)
	def __init__(self, portInstance, parent=None):
		super(protocolMonitor, self).__init__(parent)
		self.newMessageEvent = QEvent.registerEventType()
		self.portInstance = portInstance
		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)

		Compression = QHBoxLayout()
		Compression.addWidget(QLabel("Incoming Packets"))
		clearInPutButton = QPushButton("Clear Input")
		Compression.addWidget(clearInPutButton)
		Compression.addStretch()
		self.usedLayout.addLayout(Compression)

		self.inStrSignal.connect(self.updateIncomingPackets)
		self.protocolOutput = QPlainTextEdit()
		self.protocolOutput.setReadOnly(True)
		self.usedLayout.addWidget(self.protocolOutput, 2)
		clearInPutButton.clicked.connect(self.protocolOutput.clear)

		Compression = QHBoxLayout()
		Compression.addWidget(QLabel("Outgoing Packets"))
		clearOutPutButton = QPushButton("Clear Output")
		Compression.addWidget(clearOutPutButton)
		Compression.addStretch()
		self.usedLayout.addLayout(Compression)


		self.protocolInput = QPlainTextEdit()
		self.protocolInput.setReadOnly(True)
		self.usedLayout.addWidget(self.protocolInput, 1)
		self.outStrSignal.connect(self.updateOutGoingPackets)
		clearOutPutButton.clicked.connect(self.protocolInput.clear)

		for Id in Protocol.MessageIDs:
			self.portInstance.registerMessageHandler(Id, self.MonitorIncomingPrint)

		self.portInstance.registerOutGoingMessageHandler(self.MonitorOutgoingPrint)

		self.portInstance.registerPacketError(self.MonitorInComingPacketError)

		self.curLine = None

		# self.usedLayout.addStretch()
		# for i in range(5):
		# 	self.protocolOutput.appendPlainText("Hi {}".format(i))
		return

	def updateIncomingPackets(self, inStr):
		# print('sdfs', inStr)
		self.protocolOutput.appendPlainText(inStr)
		return

	def updateOutGoingPackets(self, inStr):
		# print('sdfs', inStr)
		self.protocolInput.appendPlainText(inStr)
		return

	def MonitorIncomingPrint(self, inBytes):
		Message = inBytes[1:]
		ID = inBytes[0]
		try:
			IDString = Protocol.MessageIDs(ID).name
		except ValueError:
			IDString = "Invalid ID ({})".format(ID)
		# print(IDString)
		if Protocol.MessageIDs(ID) == Protocol.MessageIDs.ID_DEBUG:
			try:
				Message = Message.decode('ascii')
			except UnicodeDecodeError:
				Message = 'Non-Ascii Characters in Message: 0X'+Message.hex().upper()
		else:
			Message = '0X'+Message.hex().upper()

		self.curLine = "{}\t{}\t{}".format(datetime.datetime.now(), IDString, Message)
		# QCoreApplication.postEvent(self, QEvent(self.newMessageEvent))
		self.inStrSignal.emit(self.curLine)

		return

	def MonitorOutgoingPrint(self, inBytes):
		ID = inBytes[2]
		try:
			IDString = Protocol.MessageIDs(ID).name
		except ValueError:
			IDString = "Invalid ID ({})".format(ID)
		curline = "{}\t{}\t0X{}".format(datetime.datetime.now(), IDString, inBytes.hex().upper())
		self.outStrSignal.emit(curline)
		return


	def MonitorInComingPacketError(self, errorMsg, inBytes):
		curline = "{}\tERROR in Packet Decoding\t{}\t0X{}".format(datetime.datetime.now(), errorMsg, inBytes.hex().upper())
		self.inStrSignal.emit(curline)
		return


