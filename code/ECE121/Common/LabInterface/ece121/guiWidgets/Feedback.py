from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from setuptools.command.test import test

from ece121 import Protocol
import sys
import enum
import random
import struct
import datetime

powerCap = 27

class testStates(enum.Enum):
	IDLE =enum.auto()
	SENDINGGAINS = enum.auto()
	RESETTINGINTEGRATOR = enum.auto()
	TESTZERO = enum.auto()
	TESTPOINTS = enum.auto()
	RATELIMITING =enum.auto()

widgetName = "Feedback Control"

class FeedBack(QWidget):
	signal = pyqtSignal(int)
	stringSignal = pyqtSignal(str)
	def __init__(self, portInstance, parent=None):
		super(FeedBack, self).__init__(parent)

		self.portInstance = portInstance
		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)

		self.startTestButton = QPushButton("start Test")
		self.usedLayout.addWidget(self.startTestButton)
		self.startTestButton.clicked.connect(self.startTest)

		self.testOutput = QPlainTextEdit()
		self.testOutput.setReadOnly(True)
		self.usedLayout.addWidget(self.testOutput)
		self.stringSignal.connect(self.updateOutput)

		self.PGain = 1
		self.IGain = 0
		self.DGain = 0
		self.AccumulatedError = 0
		self.lastSensorValue = 0


		self.testState = testStates.IDLE

		self.refValue = 0
		self.sensorValue = 0
		self.testCount = 0
		self.computedValue = 0


		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_FEEDBACK_SET_GAINS_RESP, self.AdvanceTest)
		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_FEEDBACK_RESET_CONTROLLER_RESP, self.AdvanceTest)
		self.portInstance.registerMessageHandler(Protocol.MessageIDs.ID_FEEDBACK_UPDATE_OUTPUT, self.AdvanceTest)


		# sys.exit(0)
		return


	def UpdateFeedBack(self, refInput, sensorRead):
		error = refInput - sensorRead
		self.AccumulatedError = self.AccumulatedError + error
		derivative = -(sensorRead-self.lastSensorValue)
		self.lastSensorValue = sensorRead
		output = int(self.PGain*error + self.IGain*self.AccumulatedError + self.DGain*derivative)
		if output >= 1<<powerCap:
			self.AccumulatedError = self.AccumulatedError - error
			output = 1<<powerCap
		if output <= -(1<<powerCap):
			self.AccumulatedError = self.AccumulatedError - error
			output = -(1<<powerCap)
		return output

	def AdvanceTest(self, newBytes=None):
		if newBytes is not None:
			ID = Protocol.MessageIDs(newBytes[0])
			# print(ID)
		else:
			ID = Protocol.MessageIDs.ID_INVALID
		if self.testState == testStates.IDLE:
			if newBytes is None: # this is the start case
				self.PGain = random.randint(10000, 20000)
				self.IGain = random.randint(1000, 2000)
				self.DGain = random.randint(100, 200)
				# self.DGain = 0
				self.AccumulatedError = 0
				self.lastSensorValue = 0
				self.testCount = 0
				self.refValue = random.randint(400,600)
				self.sensorValue = self.refValue
				self.portInstance.sendMessage(Protocol.MessageIDs.ID_FEEDBACK_SET_GAINS, struct.pack("!iii", self.PGain, self.IGain, self.DGain))
				self.stringSignal.emit("Setting Gains to P:{} I:{} D:{}".format(self.PGain, self.IGain, self.DGain))
				self.testState = testStates.SENDINGGAINS
		elif self.testState == testStates.SENDINGGAINS:
			if ID == Protocol.MessageIDs.ID_FEEDBACK_SET_GAINS_RESP:
				self.stringSignal.emit("Resetting Controller")
				self.portInstance.sendMessage(Protocol.MessageIDs.ID_FEEDBACK_RESET_CONTROLLER, None)
				self.testState = testStates.RESETTINGINTEGRATOR
		elif self.testState == testStates.RESETTINGINTEGRATOR:
			if ID == Protocol.MessageIDs.ID_FEEDBACK_RESET_CONTROLLER_RESP:
				self.testState = testStates.TESTZERO
				self.stringSignal.emit("Sending Test Signal of R:{} S:{}".format(self.refValue, self.sensorValue))
				self.portInstance.sendMessage(Protocol.MessageIDs.ID_FEEDBACK_UPDATE, struct.pack("!ii", self.refValue, self.sensorValue))
		elif self.testState == testStates.TESTZERO:
			if ID == Protocol.MessageIDs.ID_FEEDBACK_UPDATE_OUTPUT:
				output = struct.unpack("!i", newBytes[1:])[0]
				testOutput = self.UpdateFeedBack(self.refValue, self.sensorValue)
				if abs(output - testOutput) < 5:
					self.stringSignal.emit("Received {} and calculated {}, passed".format(output, testOutput))
				else:
					self.stringSignal.emit("Received {} and calculated {}, failed".format(output, testOutput))
					self.stringSignal.emit("Test Failed, exiting")
					self.testState = testStates.IDLE
				# print(output, testOutput)

				self.refValue += random.randint(-50, 50)
				self.sensorValue += random.randint(-50, 50)
				self.portInstance.sendMessage(Protocol.MessageIDs.ID_FEEDBACK_UPDATE, struct.pack("!ii", self.refValue, self.sensorValue))
				self.testState = testStates.TESTPOINTS
				self.testCount += 1
				# self.testState = testStates.IDLE
		elif self.testState == testStates.TESTPOINTS:
			if ID == Protocol.MessageIDs.ID_FEEDBACK_UPDATE_OUTPUT:
				output = struct.unpack("!i", newBytes[1:])[0]
				testOutput = self.UpdateFeedBack(self.refValue, self.sensorValue)
				if abs(output - testOutput) < 5:
					self.stringSignal.emit("Received {} and calculated {}, passed".format(output, testOutput))
				else:
					self.stringSignal.emit("Received {} and calculated {}, failed".format(output, testOutput))
					self.stringSignal.emit("Test Failed, exiting")
					self.testState = testStates.IDLE
				self.testCount += 1
				if self.testCount >= 10:
					self.stringSignal.emit("Test Complete at {}".format(datetime.datetime.now()))
					self.testState = testStates.IDLE
				else:
					self.refValue += random.randint(-50, 50)
					self.sensorValue += random.randint(-50, 50)
					self.stringSignal.emit("Sending Test Signal of R:{} S:{}".format(self.refValue, self.sensorValue))
					self.portInstance.sendMessage(Protocol.MessageIDs.ID_FEEDBACK_UPDATE, struct.pack("!ii", self.refValue, self.sensorValue))
		return

	def startTest(self):
		# self.portInstance.sendMessage(Protocol.MessageIDs.ID_FEEDBACK_CLEAR_INTEGRATOR, None)
		# self.sendGains()
		# self.sendStep(300, -342)
		# print(self.UpdateFeedBack(300, -342))
		self.stringSignal.emit("Test Started at {}".format(datetime.datetime.now()))
		self.testState = testStates.IDLE
		self.AdvanceTest()

		return

	def sendGains(self):
		payload = struct.pack("!iii", self.PGain, self.IGain, self.DGain)
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_FEEDBACK_SET_GAINS, payload)
		return

	def sendStep(self, reference, signal):
		payload = struct.pack("!ii", reference, signal)
		self.portInstance.sendMessage(Protocol.MessageIDs.ID_FEEDBACK_UPDATE, payload)
		return

	def updateOutput(self, str):
		self.testOutput.appendPlainText(str)
		return