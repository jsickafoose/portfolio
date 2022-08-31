
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5
from functools import partial
from ece121 import Protocol
import struct


widgetName = "Lab 5 Application"

titleFontSize = 20

class Lab5Application(QWidget):
	signal = pyqtSignal(int)
	feedbackSignal = pyqtSignal(tuple)
	newGainSignal = pyqtSignal(tuple)
	newModeSignal = pyqtSignal(int)
	def __init__(self, portInstance, parent=None):
		super(Lab5Application, self).__init__(parent)

		self.portInstance = portInstance

		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)

		sectionLabel = QLabel("Gain Settings")
		currentFont = sectionLabel.font()
		currentFont.setPointSize(titleFontSize)
		sectionLabel.setFont(currentFont)
		self.usedLayout.addWidget(sectionLabel)

		compression = QHBoxLayout()

		gainSection = QGridLayout()
		compression.addLayout(gainSection)
		self.usedLayout.addLayout(compression)


		gainValidator = QIntValidator(0, 1<<30)
		gainSection.addWidget(QLabel("Proportional Gain:"), 0, 0)
		self.PGain = QLineEdit(str(1))
		self.PGain.setValidator(gainValidator)
		gainSection.addWidget(self.PGain, 0, 1)

		gainSection.addWidget(QLabel("Integral Gain:"), 1, 0)
		self.IGain = QLineEdit(str(0))
		self.IGain.setValidator(gainValidator)
		gainSection.addWidget(self.IGain, 1, 1)

		gainSection.addWidget(QLabel("Derivative Gain:"), 2, 0)
		self.DGain = QLineEdit(str(0))
		self.DGain.setValidator(gainValidator)
		gainSection.addWidget(self.DGain, 2, 1)

		setGainButton = QPushButton("Set Gains")
		setGainButton.clicked.connect(self.sendGains)


		gainSection.addWidget(setGainButton, 3, 0, 1, 1)
		gainSection.setColumnStretch(gainSection.columnCount(), 1)

		getGainButton = QPushButton("Get Gains")
		getGainButton.clicked.connect(self.getGains)
		gainSection.addWidget(getGainButton, 3, 1, 1, 1)

		# compression.addStretch()

		line = QFrame()
		line.setFrameShape(QFrame.HLine)
		line.setFrameShadow(QFrame.Sunken)
		self.usedLayout.addWidget(line)

		sectionLabel = QLabel("Control Options")
		currentFont = sectionLabel.font()
		currentFont.setPointSize(titleFontSize)
		sectionLabel.setFont(currentFont)
		self.usedLayout.addWidget(sectionLabel)


		modeGrid = QGridLayout()
		self.usedLayout.addLayout(modeGrid)

		self.useSensorMode = QRadioButton("Sensor Input")
		modeGrid.addWidget(self.useSensorMode, 0, 0, 1, 2)
		self.useCommandMode = QRadioButton("Command Input")
		modeGrid.addWidget(self.useCommandMode, 1, 0,1, 2)

		self.setModeButton = QPushButton("Set Mode")
		modeGrid.addWidget(self.setModeButton, 2, 0)
		self.setModeButton.clicked.connect(self.sendMode)
		self.getModeButton = QPushButton("Get Mode")
		self.getModeButton.clicked.connect(self.askForMode)
		modeGrid.addWidget(self.getModeButton, 2, 1)

		modeGrid.setColumnStretch(modeGrid.columnCount(), 1)

		compression = QHBoxLayout()
		self.usedLayout.addLayout(compression)
		compression.addWidget(QLabel("Commanded Position"))
		self.PositionCommand = QLineEdit(str(1000))
		self.PositionCommand.setValidator(QIntValidator())
		compression.addWidget(self.PositionCommand)
		setRateButton = QPushButton("Set Position")
		setRateButton.clicked.connect(self.newPosition)
		compression.addWidget(setRateButton)
		motorOffButton = QPushButton("Set Position to Zero")
		motorOffButton.clicked.connect(partial(self.sendPositionCommand, 0))
		compression.addWidget(motorOffButton)
		compression.addStretch()

		self.CurrentMotorSpeed = 0

		line = QFrame()
		line.setFrameShape(QFrame.HLine)
		line.setFrameShadow(QFrame.Sunken)
		self.usedLayout.addWidget(line)

		sectionLabel = QLabel("FeedBack Report")
		currentFont = sectionLabel.font()
		currentFont.setPointSize(titleFontSize)
		sectionLabel.setFont(currentFont)
		self.usedLayout.addWidget(sectionLabel)

		feedbackReportGrid = QGridLayout()
		feedbackReportGrid.setAlignment(Qt.AlignCenter)

		self.usedLayout.addLayout(feedbackReportGrid)


		feedbackReportGrid.addWidget(QLabel("Error"), 1, 0)
		feedbackReportGrid.addWidget(QLabel("Reference"), 2, 0)
		feedbackReportGrid.addWidget(QLabel("Sensor"), 3, 0)
		feedbackReportGrid.addWidget(QLabel("Position"), 4, 0)

		feedbackReportGrid.addWidget(QLabel("Raw Value"), 0, 1, alignment=Qt.AlignCenter)
		feedbackReportGrid.addWidget(QLabel("Average"), 0, 2, alignment=Qt.AlignCenter)
		feedbackReportGrid.addWidget(QLabel("Max Value"), 0, 3, alignment=Qt.AlignCenter)
		feedbackReportGrid.addWidget(QLabel("Min Value"), 0, 4, alignment=Qt.AlignCenter)
		feedbackReportGrid.addWidget(QLabel("Peak To Peak"), 0, 5, alignment=Qt.AlignCenter)
		feedbackReportGrid.addWidget(QLabel("Average Peak to Peak"), 0, 6, alignment=Qt.AlignCenter)

		self.errorLabels = list()
		self.refLabels = list()
		self.pwmLabels = list()
		self.sensorLabels = list()
		for i in range(1, 7):
			self.errorLabels.append(QLabel("N/A"))
			feedbackReportGrid.addWidget(self.errorLabels[-1], 1, i, alignment=Qt.AlignCenter)

			self.refLabels.append(QLabel("N/A"))
			feedbackReportGrid.addWidget(self.refLabels[-1], 2, i, alignment=Qt.AlignCenter)

			self.sensorLabels.append(QLabel("N/A"))
			feedbackReportGrid.addWidget(self.sensorLabels[-1], 3, i, alignment=Qt.AlignCenter)

			self.pwmLabels.append(QLabel("N/A"))
			feedbackReportGrid.addWidget(self.pwmLabels[-1], 4, i, alignment=Qt.AlignCenter)
		feedbackReportGrid.setColumnStretch(feedbackReportGrid.columnCount(), 1)

		self.errorHistory =list()
		self.refHistory = list()
		self.pwmHistory = list()
		self.sensorHistory = list()

		self.errorPeakHistory = list()
		self.refPeakHistory = list()
		self.pwmPeakHistory = list()
		self.sensorPeakHistory =list()

		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_LAB5_REPORT, self.feedBackReport)
		self.feedbackSignal.connect(self.updateGuiFeedback)

		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_FEEDBACK_CUR_GAINS, self.reqGains)
		self.newGainSignal.connect(self.updateGuiGains)

		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_LAB5_CUR_MODE, self.newModePacket)
		self.newModeSignal.connect(self.updateGuiMode)

		self.usedLayout.addStretch()
		return

	def feedBackReport(self, newBytes):
		# print(newBytes)
		payload = newBytes[1:]
		newValues = struct.unpack("!iiii", payload)
		self.feedbackSignal.emit(newValues)
		return

	def updateGuiFeedback(self, newdataPoint):
		# print(newdataPoint)

		for i, labels, history, peakHistory, value in zip(range(4), [self.errorLabels, self.refLabels, self.sensorLabels, self.pwmLabels],
														  [self.errorHistory, self.refHistory, self. sensorHistory, self.pwmHistory],
														  [self.errorPeakHistory, self.refPeakHistory, self.sensorPeakHistory, self.pwmPeakHistory], newdataPoint):
			history.append(value)
			if len(history) > 200:
				history.pop(0)
			labels[0].setText(str(value))
			labels[1].setText(str(int(sum(history)/len(history))))
			labels[2].setText(str(max(history)))
			labels[3].setText(str(min(history)))

			peakToPeak = max(history) - min(history)
			labels[4].setText(str(peakToPeak))
			peakHistory.append(peakToPeak)
			if len(peakHistory) > 200:
				peakHistory.pop(0)
			labels[5].setText(str(int(sum(peakHistory) / len(peakHistory))))
			# print(values)

	def sendGains(self):
		try:
			payload = struct.pack("!iii", int(self.PGain.text()), int(self.IGain.text()), int(self.DGain.text()))
			self.portInstance.sendMessage(Protocol.MessageIDs.ID_FEEDBACK_SET_GAINS, payload)
		except ValueError:
			pass
		return

	def newPosition(self):
		try:
			newPosition = int(self.PositionCommand.text())
			self.sendPositionCommand(newPosition)
		except ValueError:
			pass
		return

	def sendPositionCommand(self, commandedRate):
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_COMMANDED_POSITION, struct.pack("!i", commandedRate))
		return

	def getGains(self):
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_FEEDBACK_REQ_GAINS)
		return

	def reqGains(self, newBytes):
		payload = newBytes[1:]
		self.newGainSignal.emit(struct.unpack("!iii", payload))
		return

	def updateGuiGains(self, newGains):
		self.PGain.setText(str(newGains[0]))
		self.IGain.setText(str(newGains[1]))
		self.DGain.setText(str(newGains[2]))
		return

	def newModePacket(self, newBytes):
		payload = newBytes[1:]
		newMode = struct.unpack("!b", payload)[0]
		self.newModeSignal.emit(newMode)
		return

	def updateGuiMode(self, newMode):
		if newMode == 0:
			self.useCommandMode.click()
		elif newMode == 1:
			self.useSensorMode.click()
		return

	def askForMode(self, mode):
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_LAB5_REQ_MODE)
		return

	def sendMode(self):
		if self.useCommandMode.isChecked():
			newMode = 0
		elif self.useSensorMode.isChecked():
			newMode = 1
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_LAB5_SET_MODE, struct.pack("!b", newMode))