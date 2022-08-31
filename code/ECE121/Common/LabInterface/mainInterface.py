from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import PyQt5
from ece121 import Protocol
from ece121 import guiWidgets

class mainWidget(QWidget):
	def __init__(self, portInstance, parent=None):
		super(mainWidget, self).__init__(parent)
		self.portInstance = portInstance


		self.tabs = QTabWidget()
		hmm = QVBoxLayout()
		self.outerLayout = QSplitter(Qt.Vertical)
		hmm.addWidget(self.outerLayout)
		self.setLayout(hmm)

		self.outerLayout.addWidget(self.tabs)


		self.lab1Tabs = QTabWidget()
		self.tabs.addTab(self.lab1Tabs, "Lab 1")

		self.lab2Tabs = QTabWidget()
		self.tabs.addTab(self.lab2Tabs, "Lab 2")

		self.lab3Tabs = QTabWidget()
		self.tabs.addTab(self.lab3Tabs, "Lab 3")

		self.lab4Tabs = QTabWidget()
		self.tabs.addTab(self.lab4Tabs, "Lab 4")

		self.lab5Tabs = QTabWidget()
		self.tabs.addTab(self.lab5Tabs, "Lab 5")

		self.utilityTabs = QTabWidget()
		self.tabs.addTab(self.utilityTabs, "Utilities")
		# self.lab0Tabs.addWidget()
		# self.utilityTabs.addTab(guiWidgets.protocolMonitor.protocolMonitor(self.portInstance),
		# 						guiWidgets.protocolMonitor.widgetName)
		self.lab1Tabs.addTab(guiWidgets.Lab1Application.Lab1Application(self.portInstance), guiWidgets.Lab1Application.widgetName)
		self.lab2Tabs.addTab(guiWidgets.PingSensor.PingSensor(self.portInstance),
							 guiWidgets.PingSensor.widgetName)
		self.lab2Tabs.addTab(guiWidgets.RotaryEncoder.RotaryEncoder(self.portInstance),
							 guiWidgets.RotaryEncoder.widgetName)
		self.lab2Tabs.addTab(guiWidgets.RCServo.RCServo(self.portInstance), guiWidgets.RCServo.widgetName)
		self.lab2Tabs.addTab(guiWidgets.Lab2Application.Lab2Application(self.portInstance), guiWidgets.Lab2Application.widgetName)


		self.lab3Tabs.addTab(guiWidgets.ADCReadings.ADCReadings(self.portInstance), guiWidgets.ADCReadings.widgetName)
		self.lab3Tabs.addTab(guiWidgets.NonVolatileMemory.NonVolatileMemory(self.portInstance),
							 guiWidgets.NonVolatileMemory.widgetName)
		self.lab3Tabs.addTab(guiWidgets.Lab3Application.Lab3Application(self.portInstance), guiWidgets.Lab3Application.widgetName)


		self.lab4Tabs.addTab(guiWidgets.DCMotorControl.DCMotorControl(self.portInstance),
							 guiWidgets.DCMotorControl.widgetName)
		self.lab4Tabs.addTab(guiWidgets.Feedback.FeedBack(self.portInstance), guiWidgets.Feedback.widgetName)
		self.lab4Tabs.addTab(guiWidgets.Lab4Application.Lab4Application(self.portInstance), guiWidgets.Lab4Application.widgetName)

		self.lab5Tabs.addTab(guiWidgets.Lab5PreFlight.Lab5PreFlight(self.portInstance), guiWidgets.Lab5PreFlight.widgetName)
		self.lab5Tabs.addTab(guiWidgets.Lab5Application.Lab5Application(self.portInstance), guiWidgets.Lab5Application.widgetName)

		self.utilityTabs.addTab(guiWidgets.DataLogging.DataLogging(self.portInstance), guiWidgets.DataLogging.widgetName)
		self.utilityTabs.addTab(guiWidgets.PacketBuilder.PacketBuilder(self.portInstance), guiWidgets.PacketBuilder.widgetName)



		self.tabs.addTab(guiWidgets.SerialControl.SerialControl(self.portInstance), guiWidgets.SerialControl.widgetName)

		self.tabs.setCurrentIndex(self.tabs.count()-1)
		# self.lab4Tabs.setCurrentIndex(self.lab4Tabs.count()-1)

		self.outerLayout.addWidget(guiWidgets.protocolMonitor.protocolMonitor(self.portInstance))

		return


class mainInterface(QMainWindow):

	def __init__(self, parent=None):
		super(mainInterface, self).__init__(parent)

		# self.setMinimumHeight(720)
		# self.setMinimumWidth(1280)
		self.resize(1280, 720)

		self.portInstance = Protocol.Protocol()
		self.setWindowTitle("ECE121 Main Interface")
		self.mainWindow = mainWidget(self.portInstance)
		# self.statusBar().showMessage("Active Connection: {}".format(self.portInstance.activeConnection), 1000)

		self.setCentralWidget(self.mainWindow)

		self.show()

		# we add permanent widgets to the status bar to show a variety of information
		self.serialStatus = QLabel("Hi ")
		self.packetTransmissions = QLabel(" Bob")
		self.statusBar().addPermanentWidget(self.serialStatus)
		self.statusBar().addPermanentWidget(self.packetTransmissions)

		self.updateStatus()

		self.Timer = QTimer()
		self.Timer.timeout.connect(self.updateStatus)
		self.Timer.start(100)

		# if not self.portInstance.activeConnection:
		# 	QMessageBox.information(self, "Serial Port Status", "No Serial Ports Found")
		return

	def updateStatus(self):
		if self.portInstance.activeConnection:
			self.serialStatus.setText("{} Connected".format(self.portInstance.Port))
		else:
			if self.portInstance.Port is None:
				self.serialStatus.setText("No Ports Found")
			else:
				self.serialStatus.setText("{} Disconnected".format(self.portInstance.Port))

		self.packetTransmissions.setText("Received: {} Transmitted: {}".format(self.portInstance.packetCountReceiving, self.portInstance.packetCountSending))
		return


sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, tracevalue):
	# Print the error and traceback
	import traceback
	with open("LastCrash.txt", 'w') as f:
		# f.write(repr(exctype))
		# f.write('\n')
		# f.write(repr(value))
		# f.write('\n')
		traceback.print_exception(exctype, value, tracevalue, file=f)
		# traceback.print_tb(tracevalue, file=f)
	print(exctype, value, tracevalue)
	# Call the normal Exception hook after
	sys._excepthook(exctype, value, tracevalue)
	sys.exit(0)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

app = QApplication(sys.argv)
gui = mainInterface()
gui.show()
app.exec_()