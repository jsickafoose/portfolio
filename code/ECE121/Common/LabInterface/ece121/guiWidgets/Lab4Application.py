
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5
from functools import partial
from ece121 import Protocol
import struct


widgetName = "Lab 4 Application"

titleFontSize = 20

class Lab4Application(QWidget):
	signal = pyqtSignal(int)
	feedbackSignal = pyqtSignal(tuple)
	def __init__(self, portInstance, parent=None):
		super(Lab4Application, self).__init__(parent)

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

		gainSection.addWidget(setGainButton, 3, 0, 1, 2)
		gainSection.setColumnStretch(gainSection.columnCount(), 1)
		# compression.addStretch()

		line = QFrame()
		line.setFrameShape(QFrame.HLine)
		line.setFrameShadow(QFrame.Sunken)
		self.usedLayout.addWidget(line)

		sectionLabel = QLabel("Commanded Rate")
		currentFont = sectionLabel.font()
		currentFont.setPointSize(titleFontSize)
		sectionLabel.setFont(currentFont)
		self.usedLayout.addWidget(sectionLabel)


		compression = QHBoxLayout()
		self.usedLayout.addLayout(compression)
		compression.addWidget(QLabel("Commanded Rate"))
		self.rateCommand = QLineEdit(str(1000))
		self.rateCommand.setValidator(QIntValidator())
		compression.addWidget(self.rateCommand)
		setRateButton = QPushButton("Set Rate")
		setRateButton.clicked.connect(self.newRate)
		compression.addWidget(setRateButton)
		motorOffButton = QPushButton("Set Rate to Zero")
		motorOffButton.clicked.connect(partial(self.sendRateCommand, 0))
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

		rateReportGrid = QGridLayout()
		rateReportGrid.setAlignment(Qt.AlignCenter)

		self.usedLayout.addLayout(rateReportGrid)


		rateReportGrid.addWidget(QLabel("Error"), 1, 0)
		rateReportGrid.addWidget(QLabel("Rate"), 2, 0)
		rateReportGrid.addWidget(QLabel("PWM"), 3, 0)

		rateReportGrid.addWidget(QLabel("Raw Value"), 0, 1, alignment=Qt.AlignCenter)
		rateReportGrid.addWidget(QLabel("Average"), 0, 2, alignment=Qt.AlignCenter)
		rateReportGrid.addWidget(QLabel("Max Value"), 0, 3, alignment=Qt.AlignCenter)
		rateReportGrid.addWidget(QLabel("Min Value"), 0, 4, alignment=Qt.AlignCenter)
		rateReportGrid.addWidget(QLabel("Peak To Peak"), 0, 5, alignment=Qt.AlignCenter)
		rateReportGrid.addWidget(QLabel("Average Peak to Peak"), 0, 6, alignment=Qt.AlignCenter)

		self.errorLabels = list()
		self.rateLabels = list()
		self.pwmLabels = list()
		for i in range(1, 7):
			self.errorLabels.append(QLabel("N/A"))
			rateReportGrid.addWidget(self.errorLabels[-1], 1, i, alignment=Qt.AlignCenter)

			self.rateLabels.append(QLabel("N/A"))
			rateReportGrid.addWidget(self.rateLabels[-1], 2, i, alignment=Qt.AlignCenter)

			self.pwmLabels.append(QLabel("N/A"))
			rateReportGrid.addWidget(self.pwmLabels[-1], 3, i, alignment=Qt.AlignCenter)
		rateReportGrid.setColumnStretch(rateReportGrid.columnCount(), 1)

		self.errorHistory =list()
		self.rateHistory = list()
		self.pwmHistory = list()

		self.errorPeakHistory = list()
		self.ratePeakHistory = list()
		self.pwmPeakHistory = list()

		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_REPORT_FEEDBACK, self.feedBackReport)
		self.feedbackSignal.connect(self.updateGuiFeedback)

		self.usedLayout.addStretch()
		return

	def feedBackReport(self, newBytes):
		# print(newBytes)
		payload = newBytes[1:]
		newValues = struct.unpack("!iii", payload)
		self.feedbackSignal.emit(newValues)
		return

	def updateGuiFeedback(self, newdataPoint):
		# print(newdataPoint)

		for i, labels, history, peakHistory, value in zip(range(3), [self.errorLabels, self.rateLabels, self.pwmLabels],
														  [self.errorHistory, self.rateHistory, self.pwmHistory],
														  [self.errorPeakHistory, self.ratePeakHistory, self.pwmPeakHistory], newdataPoint):
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

	def newRate(self):
		try:
			newRate = int(self.rateCommand.text())
			self.sendRateCommand(newRate)
		except ValueError:
			pass


	def sendRateCommand(self, commandedRate):
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_COMMANDED_RATE, struct.pack("!i", commandedRate))
		return