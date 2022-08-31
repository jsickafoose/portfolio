from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5


widgetName = "Serial Control"

class SerialControl(QWidget):

	def __init__(self, portInstance, parent=None):
		super(SerialControl, self).__init__(parent)

		self.portInstance = portInstance
		self.lastError = None

		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)

		statusGrid = QGridLayout()

		statusGrid.addWidget(QLabel("Serial Port: "), 0, 0)
		self.serialPortSelection = QComboBox()
		statusGrid.addWidget(self.serialPortSelection, 0, 1)
		self.rescanPorts()

		statusGrid.addWidget(QLabel("Baud Rate: "), 1, 0)
		self.baudRateLabel = QLabel(str(self.portInstance.BaudRate))
		statusGrid.addWidget(self.baudRateLabel, 1, 1)

		statusGrid.addWidget(QLabel("Status: "), 2, 0)
		self.connectionStatusLabel = QLabel("N/A")
		statusGrid.addWidget(self.connectionStatusLabel, 2, 1)

		statusGrid.addWidget(QLabel("Last Error: "), 3, 0)
		self.lastErrorLabel = QLabel(str(None))
		statusGrid.addWidget(self.lastErrorLabel, 3, 1)
		statusGrid.setColumnStretch(2, 1)

		self.usedLayout.addLayout(statusGrid)

		self.connectButton = QPushButton("Connect")
		self.connectButton.clicked.connect(self.connect)
		self.disconnectButton = QPushButton("Disconnect")
		self.disconnectButton.clicked.connect(self.disconnect)


		compression = QHBoxLayout()
		compression.addWidget(self.connectButton)
		compression.addWidget(self.disconnectButton)
		compression.addStretch()
		self.usedLayout.addLayout(compression)

		self.rescanPortsButton = QPushButton("Rescan Ports")
		self.rescanPortsButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
		self.usedLayout.addWidget(self.rescanPortsButton, Qt.AlignLeft)
		self.rescanPortsButton.clicked.connect(self.rescanPorts)
		# self.usedLayout.addLayout(compression)

		self.portInstance.registerErrorHandler(self.recordError)
		self.usedLayout.addStretch()
		self.updateStatus()

		self.Timer = QTimer()
		self.Timer.timeout.connect(self.updateStatus)
		self.Timer.start(100)

		return

	def updateStatus(self):
		"""this updates the status of the port and also enables/disables controls as appropriate"""
		if self.portInstance.activeConnection:
			# print("we are active")
			self.serialPortSelection.setDisabled(True)
			self.connectButton.setDisabled(True)
			self.disconnectButton.setDisabled(False)
			self.rescanPortsButton.setDisabled(True)
			self.connectionStatusLabel.setText("Connected")
		else:
			self.serialPortSelection.setDisabled(False)
			self.connectButton.setDisabled(False)
			self.disconnectButton.setDisabled(True)
			self.rescanPortsButton.setDisabled(False)

			if self.portInstance.Port is not None:
				self.connectionStatusLabel.setText("Disconnected")
			else:
				self.connectionStatusLabel.setText("No Port Available")
			# print("inactive")
		if self.lastError is not None:
			if str(self.lastError) != self.lastErrorLabel.text():
				self.lastErrorLabel.setText(str(self.lastError))
		return

	def connect(self):
		if self.serialPortSelection.currentText() != self.portInstance.Port:
			self.portInstance.Port = self.serialPortSelection.currentText()
		self.portInstance.Connect()
		self.updateStatus()
		return

	def disconnect(self):
		self.portInstance.Disconnect()
		self.updateStatus()
		return
	def recordError(self, inException):
		self.lastError = inException
		# self.updateStatus()
		return

	def rescanPorts(self):
		availablePorts = self.portInstance.listSerialPorts()
		self.serialPortSelection.clear()
		self.serialPortSelection.addItems(availablePorts)
		if self.serialPortSelection.findText(self.portInstance.Port) != -1:
			self.serialPortSelection.setCurrentIndex(self.serialPortSelection.findText(self.portInstance.Port))
		return
