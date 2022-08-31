from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5


widgetName = "Serial Status"

class serialStatus(QWidget):

	def __init__(self, portInstance, parent=None):
		super(serialStatus, self).__init__(parent)

		self.portInstance = portInstance

		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)

		# self.usedLayout.addWidget(QLabel("Hello Widget"))

		self.serialName = QLabel()
		self.usedLayout.addWidget(self.serialName)

		self.baudRate = QLabel()
		self.usedLayout.addWidget(self.baudRate)

		self.status = QLabel()
		self.usedLayout.addWidget(self.status)

		self.lastError = None

		self.errorStatus = QLabel()
		self.usedLayout.addWidget(self.errorStatus)
		self.portInstance.registerErrorHandler(self.recordError)

		refreshButton = QPushButton("&Refresh")

		# refreshButton.setMaximumWidth(200)
		self.usedLayout.addWidget(refreshButton)
		refreshButton.clicked.connect(self.updateStatus)

		self.toggleConnectButton = QPushButton("&Unimplemented")

		self.usedLayout.addWidget(self.toggleConnectButton)
		self.updateStatus()

		# self.usedLayout.addSpacerItem(QSpacerItem())
		self.usedLayout.addStretch()
		return

	def updateStatus(self):

		self.serialName.setText("Serial Port: {}".format(self.portInstance.Port))
		self.baudRate.setText("Baud Rate: {}".format(self.portInstance.BaudRate))

		if self.portInstance.activeConnection:
			self.status.setText("Port is connected")
		else:
			self.status.setText("Port is disconnected")

		if self.lastError is None:
			self.errorStatus.setText("No errors Reported")
		else:
			self.errorStatus.setText("Last Error: {}".format(self.lastError))

		return

	def recordError(self, inException):
		self.lastError = inException
		self.updateStatus()
		return
