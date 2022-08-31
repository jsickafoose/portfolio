
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5
from functools import partial
from ece121 import Protocol
import struct


widgetName = "Lab 5 PreFlight"

titleFontSize = 20

class Lab5PreFlight(QWidget):
	PosSignal = pyqtSignal(int)
	ADSignal = pyqtSignal(tuple)
	def __init__(self, portInstance, parent=None):
		super(Lab5PreFlight, self).__init__(parent)

		self.portInstance = portInstance

		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)

		sectionLabel = QLabel("Absolute Position")
		currentFont = sectionLabel.font()
		currentFont.setPointSize(titleFontSize)
		sectionLabel.setFont(currentFont)
		self.usedLayout.addWidget(sectionLabel)

		compression = QHBoxLayout()
		compression.addWidget(QLabel("Absolute Position: "))
		self.absPos = QLabel("N/A")
		compression.addWidget(self.absPos)
		self.usedLayout.addLayout(compression)
		compression.addStretch()

		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_ENCODER_ABS, self.inPos)
		self.PosSignal.connect(self.updatePos)

		line = QFrame()
		line.setFrameShape(QFrame.HLine)
		line.setFrameShadow(QFrame.Sunken)
		self.usedLayout.addWidget(line)

		sectionLabel = QLabel("A/D Differences")
		currentFont = sectionLabel.font()
		currentFont.setPointSize(titleFontSize)
		sectionLabel.setFont(currentFont)
		self.usedLayout.addWidget(sectionLabel)

		adcDiffGrid = QGridLayout()
		adcDiffGrid.setAlignment(Qt.AlignCenter)

		self.usedLayout.addLayout(adcDiffGrid)


		adcDiffGrid.addWidget(QLabel("Channel 1"), 1, 0)
		adcDiffGrid.addWidget(QLabel("Channel 2"), 2, 0)
		adcDiffGrid.addWidget(QLabel("P2PCH1-P2PCH2"), 3, 0)

		adcDiffGrid.addWidget(QLabel("Raw Value"), 0, 1, alignment=Qt.AlignCenter)
		adcDiffGrid.addWidget(QLabel("Average"), 0, 2, alignment=Qt.AlignCenter)
		adcDiffGrid.addWidget(QLabel("Max Value"), 0, 3, alignment=Qt.AlignCenter)
		adcDiffGrid.addWidget(QLabel("Min Value"), 0, 4, alignment=Qt.AlignCenter)
		adcDiffGrid.addWidget(QLabel("Peak To Peak"), 0, 5, alignment=Qt.AlignCenter)
		adcDiffGrid.addWidget(QLabel("Average Peak to Peak"), 0, 6, alignment=Qt.AlignCenter)

		self.channelOneLabels = list()
		self.ChannelTwoLabels = list()
		self.PToPLabels = list()
		for i in range(1, 7):
			self.channelOneLabels.append(QLabel("N/A"))
			adcDiffGrid.addWidget(self.channelOneLabels[-1], 1, i, alignment=Qt.AlignCenter)

			self.ChannelTwoLabels.append(QLabel("N/A"))
			adcDiffGrid.addWidget(self.ChannelTwoLabels[-1], 2, i, alignment=Qt.AlignCenter)

			self.PToPLabels.append(QLabel("N/A"))
			adcDiffGrid.addWidget(self.PToPLabels[-1], 3, i, alignment=Qt.AlignCenter)
		adcDiffGrid.setColumnStretch(adcDiffGrid.columnCount(), 1)

		self.chOneHistory =list()
		self.chTwoHistory = list()
		self.DiffHistory = list()

		self.chOnePeakHistory = list()
		self.chTwoPeakHistory = list()
		self.DiffPeakHistory = list()


		self.usedLayout.addStretch()

		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_LAB5_ADC, self.ADCReport)
		self.ADSignal.connect(self.updateGuiADC)

		return

	def inPos(self, newBytes):
		payload = newBytes[1:]
		self.PosSignal.emit(struct.unpack("!i", payload)[0])
		return

	def updatePos(self, newPos):
		self.absPos.setText(str(newPos))
		return


	def ADCReport(self, newBytes):
		# print(newBytes)
		payload = newBytes[1:]
		newValues = struct.unpack("!hhh", payload)
		# print(newValues)
		self.ADSignal.emit(newValues)
		return

	def updateGuiADC(self, newdataPoint):
		# print(newdataPoint)
		# newdataPoint = (newdataPoint[0], newdataPoint[1], newdataPoint[0] - newdataPoint[1])
		for i, labels, history, peakHistory, value in zip(range(3), [self.channelOneLabels, self.ChannelTwoLabels, self.PToPLabels],
														  [self.chOneHistory, self.chTwoHistory, self.DiffHistory],
														  [self.chOnePeakHistory, self.chTwoPeakHistory, self.DiffPeakHistory], newdataPoint):

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
		# self.PToPLabels[0].setText(str(int(sum(self.chOnePeakHistory) / len(self.chOnePeakHistory) - sum(self.chTwoPeakHistory) / len(self.chTwoPeakHistory))))
		# self.PToPLabels[0].setText(str(int(self.chOnePeakHistory[-1]  - self.chTwoPeakHistory[-1])))