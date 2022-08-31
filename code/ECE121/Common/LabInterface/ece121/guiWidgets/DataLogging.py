from sys import byteorder

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5
from functools import partial
from ece121 import Protocol
import datetime
import os
import queue
import threading
import time
import struct

widgetName = "Data Logging"

class DataLogging(QWidget):
	signal = pyqtSignal(int)
	def __init__(self, portInstance, parent=None):
		super(DataLogging, self).__init__(parent)

		self.portInstance = portInstance

		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)

		# we need to store a few things

		self.outQueue = queue.Queue()  # we need to write from only one thread, hence the queue, each item will be al ine in the file
		self.startTime = time.localtime() # we need to know when logging started, this is a useless value but need the class variable
		self.LoggingActive = threading.Event() # a flag to tell us when to exit the file writing thread
		self.messageToLog = None # we need to know what message we are logging so we know what variables to expect
		self.loggedLineCount = 0 # we want to show how many lines logged to ensure people know stuff is happening
		self.LoggingActive.clear()

		self.packetsLogged = 0

		messageSelectLayout = QHBoxLayout()
		self.usedLayout.addLayout(messageSelectLayout)

		messageSelectLayout.addWidget(QLabel("Select Message to Log"))

		self.messageSelect = QComboBox()
		messageSelectLayout.addWidget(self.messageSelect)
		messagesofInterest = [x.name for x in Protocol.MessageIDs if 'ID_LOG_' in x.name]
		self.messageSelect.addItems(messagesofInterest)
		self.messageSelect.addItem(Protocol.MessageIDs.ID_REPORT_RATE.name)
		self.messageSelect.addItem(Protocol.MessageIDs.ID_REPORT_FEEDBACK.name)
		self.messageSelect.addItem(Protocol.MessageIDs.ID_LAB5_REPORT.name)
		messageSelectLayout.addStretch()

		fileSelectLayout = QHBoxLayout()
		self.usedLayout.addLayout(fileSelectLayout)
		self.selectedFilePath = QLineEdit()
		fileSelectLayout.addWidget(self.selectedFilePath)

		self.browseButton = QPushButton("&Browse")
		fileSelectLayout.addWidget(self.browseButton)
		self.browseButton.clicked.connect(self.askForFilePath)

		fileSelectLayout.addStretch()

		self.usedLayout.addWidget(QLabel("WARNING: Files are opened in write mode"))

		controlsLayout = QHBoxLayout()
		self.usedLayout.addLayout(controlsLayout)

		self.startButton = QPushButton('Start Logging')
		self.startButton.clicked.connect(self.startLogging)
		controlsLayout.addWidget(self.startButton)

		self.stopButton = QPushButton('Stop Logging')
		controlsLayout.addWidget(self.stopButton)
		self.stopButton.clicked.connect(self.stopLogging)
		self.stopButton.setDisabled(True)

		self.genFileNameButton = QPushButton('Generate FileName')
		controlsLayout.addWidget(self.genFileNameButton)
		self.genFileNameButton.clicked.connect(self.updateFileName)

		controlsLayout.addStretch()

		self.statusLabel = QLabel("Idle")
		self.usedLayout.addWidget(self.statusLabel)

		self.packetsLoggedLabel = QLabel("Packets Logged: 0")
		self.usedLayout.addWidget(self.packetsLoggedLabel)
		# self.ADValue = QLabel()
		# self.usedLayout.addWidget(self.ADValue)

		# self.signal.connect(self.updateGui)

		# self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_LOG_INT_ONE, self.newValue)
		# self.signal.connect(self.updateGui)
		# self.usedLayout.addSpacerItem(QSpacerItem())
		self.usedLayout.addStretch()

		self.selectedFilePath.setText(self.generateFileName())
		QCoreApplication.instance().aboutToQuit.connect(self.stopLogging)
		self.signal.connect(self.updatePacketCount)

		return

	def handleGuiExit(self):
		'''tiny function to handle closing the file if the gui is closed before the file is'''
		return

	def dataIn(self, newValue):
		return

	def updatePacketCount(self, newReading):
		self.packetsLoggedLabel.setText("Packets Logged: {}".format(newReading))
		return

	def startLogging(self):
		print('Starting log data')
		self.statusLabel.setText("Logging {} to {}".format(self.messageSelect.currentText(), self.selectedFilePath.text()))
		self.toggleGui(True)
		self.LoggingActive.set()
		self.packetsLogged = 0
		# threading.Thread(target=self.loggingThread).start()
		print('logging started')
		self.messageToLog = Protocol.MessageIDs[self.messageSelect.currentText()]
		# print(packetOfInterest)
		self.portInstance.registerMessageHandler(self.messageToLog, self.handleIncomingPackets)
		return

	def stopLogging(self):
		# self.exitFlag.set()
		if self.LoggingActive.is_set():
			print('Stopping data log')
			self.portInstance.deregisterMessageHandler(self.messageToLog, self.handleIncomingPackets)
			try:
				f = open(self.selectedFilePath.text(), 'w')
			except PermissionError:
				newFilePath = self.generateFileName()
				f = open(newFilePath, 'w')
				self.selectedFilePath.setText(newFilePath)
			while self.outQueue.qsize() > 0:
				incomingPacket = self.outQueue.get(block=False)
				f.write("{}\n".format(','.join([str(x) for x in incomingPacket])))
			self.statusLabel.setText("Idle")
			self.toggleGui(False)
			f.close()

			self.LoggingActive.clear()

		return

	def loggingThread(self):
		# print('Starting file operations')

		packetsLogged = 0

		self.messageToLog = Protocol.MessageIDs[self.messageSelect.currentText()]
		# print(packetOfInterest)
		timeStarted = datetime.datetime.now()
		self.portInstance.registerMessageHandler(self.messageToLog, self.handleIncomingPackets)
		# with open(self.selectedFilePath.text(),'w') as f:
		f = open(self.selectedFilePath.text(), 'w')
		while True:
			if self.LoggingActive.is_set():
				break
			if self.outQueue.qsize() > 0:
				incomingPacket = self.outQueue.get(block=False)
				packetsLogged += 1
				# if packetsLogged % 10 == 0:
				# 	self.signal.emit(packetsLogged)
				f.write("{},{}\n".format((datetime.datetime.now()-timeStarted).total_seconds(), ','.join([str(x) for x in incomingPacket])))
					# f.flush()
		f.close()
		self.portInstance.deregisterMessageHandler(self.messageToLog, self.handleIncomingPackets)
		self.LoggingActive.clear()
		print('Ending file Operations')
		return

	def handleIncomingPackets(self, inBytes):
		payload = inBytes[1:]
		if self.messageToLog is Protocol.MessageIDs.ID_LOG_INT_ONE:
			payload = int.from_bytes(payload, byteorder='little')
			self.outQueue.put([payload])
		if self.messageToLog is Protocol.MessageIDs.ID_LOG_INT_TWO:
			values = struct.unpack("<ii", payload) # little ended payload
			self.outQueue.put(values)
		if self.messageToLog is Protocol.MessageIDs.ID_REPORT_FEEDBACK:
			values = struct.unpack("!iii", payload)
			self.outQueue.put(values)
		if self.messageToLog is Protocol.MessageIDs.ID_REPORT_RATE:
			values = struct.unpack("!i", payload)
			self.outQueue.put(values)
		if self.messageToLog is Protocol.MessageIDs.ID_LAB5_REPORT:
			values = struct.unpack("!iiii", payload)
			self.outQueue.put(values)

		self.packetsLogged +=1
		if self.packetsLogged % 10 == 0:
			self.signal.emit(self.packetsLogged)

		return

	def toggleGui(self, logging):
		self.startButton.setDisabled(logging)
		self.messageSelect.setDisabled(logging)
		self.selectedFilePath.setDisabled(logging)
		self.browseButton.setDisabled(logging)
		self.stopButton.setDisabled(not logging)

		return

	def generateFileName(self):
		currentFilePath = self.selectedFilePath.text()
		folderInfo = os.path.split(currentFilePath)
		# print(folderInfo)
		if not os.path.exists(folderInfo[0]):
			folder = os.path.expanduser('~')
		else:
			folder = folderInfo[0]
		# print(folder)
		# print(self.messageSelect.currentIndex())
		selectedPacket = self.messageSelect.currentText()
		# selectedPacket = selectedPacket[len("ID_LOG_"):]
		# print(selectedPacket)
		timeString = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
		# print(timeString)
		filePath = os.path.join(folder, "{}-{}.csv".format(selectedPacket, timeString))
		# print(filePath)
		return filePath

	def updateFileName(self):
		self.selectedFilePath.setText(self.generateFileName())
		return

	def askForFilePath(self):
		fileSelect = QFileDialog()

		fileSelect.setFileMode(QFileDialog.AnyFile)
		fileSelect.setAcceptMode(QFileDialog.AcceptSave)
		folder, file = os.path.split(self.generateFileName())
		fileSelect.setDirectory(folder)
		fileSelect.selectFile(file)
		if fileSelect.exec():
			print('woo')
			wantedFile = fileSelect.selectedFiles()[0]
			self.selectedFilePath.setText(wantedFile)


		return